import json
import logging
from copy import deepcopy
from typing import Any, List, Union

from google.protobuf.json_format import MessageToDict
from nibiru_proto.proto.cosmos.base.abci.v1beta1 import abci_pb2 as abci_type
from nibiru_proto.proto.cosmos.base.v1beta1 import coin_pb2 as cosmos_base_coin_pb

from nibiru.client import GrpcClient
from nibiru.common import GAS_PRICE, PythonMsg, TxConfig, TxType
from nibiru.exceptions import SimulationError, TxError
from nibiru.network import Network
from nibiru.transaction import Transaction
from nibiru.wallet import PrivateKey


class BaseTxClient:
    def __init__(
        self,
        priv_key: PrivateKey,
        network: Network,
        client: GrpcClient,
        config: TxConfig,
    ):
        self.priv_key = priv_key
        self.network = network
        self.client = client
        self.address = None
        self.config = config

    def execute_msgs(
        self,
        msgs: Union[PythonMsg, List[PythonMsg]],
        get_sequence_from_node: bool = False,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Execute a message to broadcast a transaction to the node.
        Simulate the message to generate the gas estimate and send it to the node.
        If the transaction fail because of account sequence mismatch, we try to send it
        again once more with the sequence coming from a query to the lcd endpoint.

        Args:
            get_sequence_from_node (bool, optional): Specifies whether the sequence
                comes from the local value or the lcd endpoint. Defaults to False.

        Raises:
            TxError: Raw error log from the blockchain if the response code is nonzero.

        Returns:
            dict[str, Any]: The transaction response as a dict in proto3 JSON format.
        """
        if not isinstance(msgs, list):
            msgs = [msgs]

        pb_msgs = [msg.to_pb() for msg in msgs]

        address = None
        sequence_args = {}
        if get_sequence_from_node:
            sequence_args = {
                "from_node": True,
                "lcd_endpoint": self.network.lcd_endpoint,
            }

        try:
            self.client.sync_timeout_height()
            address = self.get_address_info()
            tx = (
                Transaction()
                .with_messages(pb_msgs)
                .with_sequence(address.get_sequence(**sequence_args))
                .with_account_num(address.get_number())
                .with_chain_id(self.network.chain_id)
                .with_signer(self.priv_key)
            )
            sim_res = self.simulate(tx)
            gas_estimate = sim_res.gas_info.gas_used
            tx_output: abci_type.TxResponse = self.execute_tx(
                tx, gas_estimate, **kwargs
            )

            if tx_output.code != 0:
                address.decrease_sequence()
                raise TxError(tx_output.raw_log)

            tx_output: dict[str, Any] = MessageToDict(tx_output)

            # Convert raw log into a dictionary
            tx_output["rawLog"] = json.loads(tx_output.get("rawLog", "{}"))
            return tx_output

        except SimulationError as err:
            if (
                "account sequence mismatch, expected" in str(err)
                and not get_sequence_from_node
            ):
                return self.execute_msgs(*msgs, get_sequence_from_node=True, **kwargs)

            if address:
                address.decrease_sequence()

            raise SimulationError(f"Failed to simulate transaction: {err}") from err

    def execute_tx(
        self, tx: Transaction, gas_estimate: float, **kwargs
    ) -> abci_type.TxResponse:
        conf = self.get_config(**kwargs)
        gas_wanted = gas_estimate * 1.25
        if conf.gas_wanted > 0:
            gas_wanted = conf.gas_wanted
        elif conf.gas_multiplier > 0:
            gas_wanted = gas_estimate * conf.gas_multiplier
        gas_price = GAS_PRICE if conf.gas_price <= 0 else conf.gas_price

        fee = [
            cosmos_base_coin_pb.Coin(
                amount=str(int(gas_price * gas_wanted)),
                denom=self.network.fee_denom,
            )
        ]
        logging.info(
            "Executing transaction with fee: %s and gas_wanted: %d", fee, gas_wanted
        )
        tx = (
            tx.with_gas(gas_wanted)
            .with_fee(fee)
            .with_memo("")
            .with_timeout_height(self.client.timeout_height)
        )
        tx_raw_bytes = tx.get_signed_tx_data()

        return self._send_tx(tx_raw_bytes, conf.tx_type)

    def _send_tx(self, tx_raw_bytes, tx_type: TxType) -> abci_type.TxResponse:
        if tx_type == TxType.SYNC:
            return self.client.send_tx_sync_mode(tx_raw_bytes)
        elif tx_type == TxType.ASYNC:
            return self.client.send_tx_async_mode(tx_raw_bytes)

        return self.client.send_tx_block_mode(tx_raw_bytes)

    def simulate(self, tx: Transaction):
        sim_tx_raw_bytes = tx.get_signed_tx_data()

        (sim_res, success) = self.client.simulate_tx(sim_tx_raw_bytes)
        if not success:
            raise SimulationError(sim_res)

        return sim_res

    def get_address_info(self):
        if self.address is None:
            pub_key = self.priv_key.to_public_key()
            self.address = pub_key.to_address()
            self.address.init_num_seq(self.network.lcd_endpoint)

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
