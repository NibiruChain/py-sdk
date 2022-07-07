
from google.protobuf import message

from nibiru.client import Client
from nibiru.composer import Composer

from nibiru.constant import GAS_PRICE
from nibiru.exceptions import SimulationError

from nibiru.network import Network
from nibiru.transaction import Transaction
from nibiru.wallet import PrivateKey


class Tx:
    def __init__(self, priv_key: PrivateKey, network: Network, client: Client):
        self.priv_key = priv_key
        self.network = network
        self.client = client
        self.address = None

    async def execute(self, msg: message.Message):
        # should this happen on every execution or only once at the beginning??
        await self.client.sync_timeout_height()
        address = await self.get_address_info()
        tx = (
            Transaction()
            .with_messages(msg)
            .with_sequence(address.get_sequence())
            .with_account_num(address.get_number())
            .with_chain_id(self.network.chain_id)
            .with_signer(self.priv_key)
        )
        try:
            sim_res = await self.simulate(tx)
        except SimulationError as err:
            print("Aborting execution due to error: {}".format(err))
        else:
            gas_wanted = sim_res.gas_info.gas_used * 1.25
            return await self.execute_tx(tx, gas_wanted)


    async def execute_tx(self, tx: Transaction, gas_wanted: float):
            fee = [Composer.Coin(
                amount=int(GAS_PRICE * gas_wanted),
                denom=self.network.fee_denom,
            )]
            tx = tx.with_gas(gas_wanted).with_fee(fee).with_memo('').with_timeout_height(self.client.timeout_height)
            tx_raw_bytes = tx.get_signed_tx_data()

            # broadcast tx: send_tx_async_mode, send_tx_sync_mode, send_tx_block_mode
            return await self.client.send_tx_block_mode(tx_raw_bytes)


    async def simulate(self, tx: Transaction):
        sim_tx_raw_bytes = tx.get_signed_tx_data()

        (sim_res, success) = await self.client.simulate_tx(sim_tx_raw_bytes)
        if not success:
            raise SimulationError("failed to simulate tx : {}".format(sim_res))

        return sim_res

    async def get_address_info(self):
        if self.address is None:
            pub_key = self.priv_key.to_public_key()
            self.address = await pub_key.to_address().async_init_num_seq(self.network.lcd_endpoint)

        return self.address