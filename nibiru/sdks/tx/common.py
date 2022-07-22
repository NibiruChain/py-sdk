import logging
from copy import deepcopy

from google.protobuf import message
from grpc import RpcError

from nibiru.client import Client
from nibiru.common import TxConfig, TxType
from nibiru.composer import Composer
from nibiru.constant import GAS_PRICE
from nibiru.exceptions import SimulationError, TxError
from nibiru.network import Network
from nibiru.transaction import Transaction
from nibiru.wallet import PrivateKey


class Tx:
    def __init__(self, priv_key: PrivateKey, network: Network, client: Client, config: TxConfig):
        self.priv_key = priv_key
        self.network = network
        self.client = client
        self.address = None
        self.config = config
        self.msgs = []

    def add_messages(self, *msgs: message.Message):
        self.msgs.extend(msgs)
        return self

    def execute(self, **kwargs):
        try:
            res = self.execute_msg(*self.msgs, **kwargs)
        except SimulationError as err:
            raise err
        else:
            self.msgs = []

        return res

    def execute_msg(self, *msg: message.Message, **kwargs):
        address = None
        try:
            # TODO: It shouldn't be necessary to resync the block height for every tx, use bgTask instead
            self.client.sync_timeout_height()
            address = self.get_address_info()
            tx = (
                Transaction()
                .with_messages(*msg)
                .with_sequence(address.get_sequence())
                .with_account_num(address.get_number())
                .with_chain_id(self.network.chain_id)
                .with_signer(self.priv_key)
            )
            sim_res = self.simulate(tx)
            gas_estimate = sim_res.gas_info.gas_used
            return self.execute_tx(tx, gas_estimate, **kwargs)
        except (RpcError, SimulationError) as err:
            logging.error("Failed tx execution: %s", err)
            if address:
                address.decrease_sequence()
            raise TxError("Failed to execute transaction") from err

    def execute_tx(self, tx: Transaction, gas_estimate: float, **kwargs):
        conf = self.get_config(**kwargs)
        gas_wanted = gas_estimate * 1.25
        if conf.gas_wanted > 0:
            gas_wanted = conf.gas_wanted
        elif conf.gas_multiplier > 0:
            gas_wanted = gas_estimate * conf.gas_multiplier
        gas_price = GAS_PRICE if conf.gas_price <= 0 else conf.gas_price

        fee = [
            Composer.coin(
                amount=int(gas_price * gas_wanted),
                denom=self.network.fee_denom,
            )
        ]
        logging.info("Executing transaction with fee: %s and gas_wanted: %d", fee, gas_wanted)
        tx = tx.with_gas(gas_wanted).with_fee(fee).with_memo("").with_timeout_height(self.client.timeout_height)
        tx_raw_bytes = tx.get_signed_tx_data()

        return self._send_tx(tx_raw_bytes, conf.tx_type)

    def _send_tx(self, tx_raw_bytes, tx_type: TxType):
        if tx_type == TxType.SYNC:
            return self.client.send_tx_sync_mode(tx_raw_bytes)
        elif tx_type == TxType.ASYNC:
            return self.client.send_tx_async_mode(tx_raw_bytes)

        return self.client.send_tx_block_mode(tx_raw_bytes)

    def simulate(self, tx: Transaction):
        sim_tx_raw_bytes = tx.get_signed_tx_data()

        (sim_res, success) = self.client.simulate_tx(sim_tx_raw_bytes)
        if not success:
            raise SimulationError("failed to simulate tx : {}".format(sim_res))

        return sim_res

    def get_address_info(self):
        if self.address is None:
            pub_key = self.priv_key.to_public_key()
            self.address = pub_key.to_address().init_num_seq(self.network.lcd_endpoint)

        return self.address

    def get_config(self, **kwargs):
        """
        Properties in kwargs overwrite config
        """
        c = deepcopy(self.config)
        props = dir(c)
        for (k, v) in kwargs.items():
            if k in props:
                setattr(c, k, v)
            else:
                logging.warning("%s is not a supported config property, ignoring", k)

        return c
