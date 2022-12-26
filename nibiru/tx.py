"""

Classes:
    TxClient
    Transaction

"""
import json
import logging
from copy import deepcopy
from numbers import Number
from typing import Any, Iterable, List, Tuple, Union

from google.protobuf import any_pb2, message
from google.protobuf.json_format import MessageToDict
from nibiru_proto.proto.cosmos.base.abci.v1beta1 import abci_pb2 as abci_type
from nibiru_proto.proto.cosmos.base.v1beta1 import coin_pb2 as cosmos_base_coin_pb
from nibiru_proto.proto.cosmos.base.v1beta1.coin_pb2 import Coin
from nibiru_proto.proto.cosmos.tx.signing.v1beta1 import signing_pb2 as tx_sign
from nibiru_proto.proto.cosmos.tx.v1beta1 import tx_pb2 as cosmos_tx_type

from nibiru import pytypes as pt
from nibiru import wallet
from nibiru.exceptions import SimulationError, TxError
from nibiru.grpc_client import GrpcClient


class TxClient:
    def __init__(
        self,
        priv_key: wallet.PrivateKey,
        network: pt.Network,
        client: GrpcClient,
        config: pt.TxConfig,
    ):
        self.priv_key = priv_key
        self.network = network
        self.client = client
        self.address = None
        self.config = config

    def execute_msgs(
        self,
        msgs: Union[pt.PythonMsg, List[pt.PythonMsg]],
        get_sequence_from_node: bool = False,
        **kwargs,
    ) -> pt.RawTxResp:
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
            Union[RawTxResp, Dict[str, Any]]: The transaction response as a dict
                in proto3 JSON format.
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
            gas_estimate: float = sim_res.gas_info.gas_used
            tx_output: abci_type.TxResponse = self.execute_tx(
                tx, gas_estimate, **kwargs
            )

            if tx_output.code != 0:
                address.decrease_sequence()
                raise TxError(tx_output.raw_log)

            tx_output: dict[str, Any] = MessageToDict(tx_output)

            # Convert raw log into a dictionary
            tx_output["rawLog"] = json.loads(tx_output.get("rawLog", "{}"))
            return pt.RawTxResp(tx_output)

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
        self, tx: "Transaction", gas_estimate: float, **kwargs
    ) -> abci_type.TxResponse:
        conf: pt.TxConfig = self.get_config(**kwargs)

        def compute_gas_wanted() -> float:
            gas_wanted = gas_estimate * 1.25  # apply gas multiplier
            if conf.gas_wanted > 0:
                gas_wanted = conf.gas_wanted
            elif conf.gas_multiplier > 0:
                gas_wanted = gas_estimate * conf.gas_multiplier
            return gas_wanted

        gas_wanted = compute_gas_wanted()
        gas_price = pt.GAS_PRICE if conf.gas_price <= 0 else conf.gas_price

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

    def _send_tx(self, tx_raw_bytes, tx_type: pt.TxType) -> abci_type.TxResponse:
        if tx_type == pt.TxType.SYNC:
            return self.client.send_tx_sync_mode(tx_raw_bytes)
        elif tx_type == pt.TxType.ASYNC:
            return self.client.send_tx_async_mode(tx_raw_bytes)

        return self.client.send_tx_block_mode(tx_raw_bytes)

    def simulate(self, tx: "Transaction"):
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

    def get_config(self, **kwargs) -> pt.TxConfig:
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


class Transaction:
    """
    Transactions trigger state changes based on messages ('msgs'). Each message
    must be signed before being broadcasted to the network, included in a block,
    validated, and approved through the consensus process.

    Attributes:
        account_num (int): Number of the account in state. Account numbers
            increment every time an account is created so that each account has
            its own number, and the highest account number is equivalent to the
            number of accounts in the 'auth' module (but not necessarily the store).
        msgs: A List of messages to be executed.
        sequence: int = None, TODO
        chain_id (str): The unique identifier for the blockchain that this
            transaction targets. Inclusion of a 'chain_id' prevents potential
            attackers from using signed transactions on other blockchains.
        fee: List[Coin] = None, TODO
        gas (int): TODO
        priv_key (wallet.PrivateKey): Primary signer for the transaction. By
            convention, the signer from the first message is referred to as the
            primary signer and pays the fee for the whole transaction. We refer
            to this primary signer with 'priv_key'.
        memo (str): Memo is a note or comment to be added to the transction.
        timeout_height (int): Timeout height is the block height after which the
            transaction will not be processed by the chain.

    """

    def __init__(
        self,
        msgs: Tuple[message.Message, ...] = None,
        account_num: int = None,
        priv_key: wallet.PrivateKey = None,
        sequence: int = None,
        chain_id: str = None,
        fee: List[Coin] = None,
        gas: int = 0,
        memo: str = "",
        timeout_height: int = 0,
    ):
        self.msgs = self.__convert_msgs(msgs) if msgs is not None else []
        self.account_num = account_num
        self.priv_key = priv_key
        self.sequence = sequence
        self.chain_id = chain_id
        self.fee = cosmos_tx_type.Fee(amount=fee, gas_limit=gas)
        self.gas = gas
        self.memo = memo
        self.timeout_height = timeout_height

    @staticmethod
    def __convert_msgs(msgs: List[message.Message]) -> List[any_pb2.Any]:
        any_msgs: List[any_pb2.Any] = []
        for msg in msgs:
            any_msg = any_pb2.Any()
            any_msg.Pack(msg, type_url_prefix="")
            any_msgs.append(any_msg)
        return any_msgs

    def with_messages(self, msgs: Iterable[message.Message]) -> "Transaction":
        self.msgs.extend(self.__convert_msgs(msgs))
        return self

    def with_sender(self, client: GrpcClient, sender: str) -> "Transaction":
        if len(self.msgs) == 0:
            raise IndexError(
                "messsage is empty, please use with_messages at least 1 message"
            )
        account = client.get_account(sender)
        if account:
            self.account_num = account.account_number
            self.sequence = account.sequence
            return self
        raise KeyError("Account doesn't exist")

    def with_signer(self, priv_key: wallet.PrivateKey):
        self.priv_key = priv_key
        return self

    def with_account_num(self, account_num: int) -> "Transaction":
        self.account_num = account_num
        return self

    def with_sequence(self, sequence: int) -> "Transaction":
        self.sequence = sequence
        return self

    def with_chain_id(self, chain_id: str) -> "Transaction":
        self.chain_id = chain_id
        return self

    def with_fee(self, fee: List[Coin]) -> "Transaction":
        self.fee = cosmos_tx_type.Fee(amount=fee, gas_limit=self.fee.gas_limit)
        return self

    def with_gas(self, gas: Number) -> "Transaction":
        self.fee.gas_limit = int(gas)
        return self

    def with_memo(self, memo: str) -> "Transaction":
        if len(memo) > pt.MAX_MEMO_CHARACTERS:
            raise ValueError("memo is too large")
        self.memo = memo
        return self

    def with_timeout_height(self, timeout_height: int) -> "Transaction":
        self.timeout_height = timeout_height
        return self

    def __generate_info(self, public_key: wallet.PublicKey = None) -> Tuple[str, str]:
        body = cosmos_tx_type.TxBody(
            messages=self.msgs, memo=self.memo, timeout_height=self.timeout_height
        )

        body_bytes = body.SerializeToString()
        mode_info = cosmos_tx_type.ModeInfo(
            single=cosmos_tx_type.ModeInfo.Single(mode=tx_sign.SIGN_MODE_DIRECT)
        )

        if public_key:
            any_public_key = any_pb2.Any()
            any_public_key.Pack(public_key.to_public_key_proto(), type_url_prefix="")
            signer_info = cosmos_tx_type.SignerInfo(
                mode_info=mode_info, sequence=self.sequence, public_key=any_public_key
            )
        else:
            signer_info = cosmos_tx_type.SignerInfo(
                mode_info=mode_info, sequence=self.sequence
            )

        auth_info = cosmos_tx_type.AuthInfo(signer_infos=[signer_info], fee=self.fee)
        auth_info_bytes = auth_info.SerializeToString()

        return body_bytes, auth_info_bytes

    def get_sign_doc(
        self, public_key: wallet.PublicKey = None
    ) -> cosmos_tx_type.SignDoc:
        if len(self.msgs) == 0:
            raise ValueError("message is empty")

        if self.account_num is None:
            raise RuntimeError("account_num should be defined")

        if self.sequence is None:
            raise RuntimeError("sequence should be defined")

        if self.chain_id is None:
            raise RuntimeError("chain_id should be defined")

        body_bytes, auth_info_bytes = self.__generate_info(public_key)

        return cosmos_tx_type.SignDoc(
            body_bytes=body_bytes,
            auth_info_bytes=auth_info_bytes,
            chain_id=self.chain_id,
            account_number=self.account_num,
        )

    def get_tx_data(
        self, signature: bytes, public_key: wallet.PublicKey = None
    ) -> bytes:
        body_bytes, auth_info_bytes = self.__generate_info(public_key)

        tx_raw = cosmos_tx_type.TxRaw(
            body_bytes=body_bytes,
            auth_info_bytes=auth_info_bytes,
            signatures=[signature],
        )
        return tx_raw.SerializeToString()

    def get_signed_tx_data(self) -> bytes:
        if self.priv_key is None:
            raise RuntimeError("priv_key should be defined")

        pub_key = self.priv_key.to_public_key()
        sign_doc = self.get_sign_doc(pub_key)
        sig = self.priv_key.sign(sign_doc.SerializeToString())
        return self.get_tx_data(sig, pub_key)
