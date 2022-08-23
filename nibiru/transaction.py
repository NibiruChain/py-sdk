from numbers import Number
from typing import Iterable, List, Tuple

from google.protobuf import any_pb2, message
from nibiru_proto.proto.cosmos.base.v1beta1.coin_pb2 import Coin
from nibiru_proto.proto.cosmos.tx.signing.v1beta1 import signing_pb2 as tx_sign
from nibiru_proto.proto.cosmos.tx.v1beta1 import tx_pb2 as cosmos_tx_type

from nibiru.client import GrpcClient
from nibiru.common import MAX_MEMO_CHARACTERS
from nibiru.wallet import PrivateKey, PublicKey


class Transaction:
    def __init__(
        self,
        msgs: Tuple[message.Message, ...] = None,
        account_num: int = None,
        priv_key: PrivateKey = None,
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

    def with_signer(self, priv_key: PrivateKey):
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
        if len(memo) > MAX_MEMO_CHARACTERS:
            raise ValueError("memo is too large")
        self.memo = memo
        return self

    def with_timeout_height(self, timeout_height: int) -> "Transaction":
        self.timeout_height = timeout_height
        return self

    def __generate_info(self, public_key: PublicKey = None) -> Tuple[str, str]:
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

    def get_sign_doc(self, public_key: PublicKey = None) -> cosmos_tx_type.SignDoc:
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

    def get_tx_data(self, signature: bytes, public_key: PublicKey = None) -> bytes:
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
