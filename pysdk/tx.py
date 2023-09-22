"""
Classes:
    TxClient: A client for building, simulating, and broadcasting transactions.
    Transaction: Transactions trigger state changes based on messages. Each
        message must be cryptographically signed before being broadcasted to
        the network.
"""
import logging
import pprint
from numbers import Number
from typing import Iterable, List, Optional, Tuple, Union

from google.protobuf import any_pb2, message

# from google.protobuf.json_format import MessageToDict
from nibiru_proto.cosmos.base.abci.v1beta1 import abci_pb2 as abci_type
from nibiru_proto.cosmos.base.v1beta1 import coin_pb2 as cosmos_base_coin_pb
from nibiru_proto.cosmos.base.v1beta1.coin_pb2 import Coin
from nibiru_proto.cosmos.tx.signing.v1beta1 import signing_pb2 as tx_sign
from nibiru_proto.cosmos.tx.v1beta1 import service_pb2 as tx_service
from nibiru_proto.cosmos.tx.v1beta1 import tx_pb2 as cosmos_tx_type

from pysdk import exceptions, jsonrpc
from pysdk import pytypes as pt
from pysdk import tmrpc, wallet
from pysdk.exceptions import SimulationError, TxError
from pysdk.grpc_client import GrpcClient


class TxClient:
    """
    A client for building, simulating, and broadcasting transactions.

    Attributes:
        address (Optional[wallet.Address])
        client (GrpcClient)
        network (pt.Network)
        priv_key (wallet.PrivateKey)
        tx_config (pt.TxConfig)

    """

    address: Optional[wallet.Address]
    client: GrpcClient
    network: pt.Network
    priv_key: wallet.PrivateKey
    tx_config: pt.TxConfig

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
        self.tx_config = config

    def execute_msgs(
        self,
        msgs: Union[pt.PythonMsg, List[pt.PythonMsg]],
        sequence: Optional[int] = None,
        tx_config: Optional[pt.TxConfig] = None,
    ) -> pt.ExecuteTxResp:
        """
        Broadcasts messages to a node in a single transaction. This function
        first simulates the corresponding transaction to estimate the amount of
        gas needed.

        If the transaction fails because of account sequence mismatch, we try
        to query the sequence from the LCD endpoint and broadcast with the
        updated sequence value.

        Args:
            msgs (Union[pt.PythonMsg, List[pt.PythonMsg]]):
            sequence (Optional[int]): Account sequence for the tx. Sequence
                is used to enforce tx ordering and prevent double-spending.
                Each time a tx is procesed and committed to the blockchain,
                the account sequence number is incremented.
            tx_config (Optional[pt.TxConfig] = None)
            get_sequence_from_node (bool, optional): Specifies whether the
                sequence comes from the local value or the lcd endpoint.
                Defaults to False.

        Raises:
            SimulationError: If broadcasting fails during the simulation.
            TxError: If the response code is nonzero, the 'TxError' includes
                the raw error logs from the blockchain.

        Returns:
            Union[RawSyncTxResp, Dict[str, Any]]: The transaction response as
                a dict in proto3 JSON format.
        """

        tx: Transaction
        address: wallet.Address = self.ensure_address_info()
        tx, address = self.build_tx(
            msgs=msgs,
        )

        # Validate account sequence
        if sequence is None:
            sequence = address.sequence
        sequence_err: str = "sequence was not given or available on the wallet object."
        assert address, sequence_err
        assert sequence, sequence_err

        tx = tx.with_sequence(sequence=sequence)

        try:
            sim_res = self.simulate(tx)
            gas_estimate: float = sim_res.gas_info.gas_used
        except SimulationError as err:
            if "account sequence mismatch, expected" in str(err):
                if not isinstance(msgs, list):
                    msgs = [msgs]
                # self.client.wait_for_next_block()
                err_str = str(err)
                want_seq = int(err_str.split("expected ")[1].split(",")[0])
                sequence = want_seq

                return self.execute_msgs(
                    msgs=msgs,
                    sequence=sequence,
                    tx_config=tx_config,
                )
            if address:
                address.decrease_sequence()
            raise SimulationError(f"Failed to simulate transaction: {err}") from err

        try:
            jsonrcp_resp: jsonrpc.JsonRPCResponse = self.execute_tx(
                tx=tx,
                gas_estimate=gas_estimate,
                tx_config=tx_config,
                use_tmrpc=True,
            )
            execute_resp = pt.ExecuteTxResp(
                code=jsonrcp_resp.result.get("code"),
                tx_hash=jsonrcp_resp.result.get("hash"),
                log=jsonrcp_resp.result.get("log"),
            )
            if execute_resp.code != 0:
                address.decrease_sequence()
                raise TxError(execute_resp.log)
            return execute_resp
            # ------------------------------------------------
            # gRPC version: TODO - add back as feature.
            # ------------------------------------------------
            # tx_resp: dict[str, Any] = MessageToDict(tx_resp)
            # tx_hash: Union[str, None] = tx_resp.get("txhash")
            # assert tx_hash, f"null txhash on tx_resp: {tx_resp}"
            # tx_output: tx_service.GetTxResponse = self.client.tx_by_hash(
            #     tx_hash=tx_hash
            # )
            #
            # if tx_output.get("tx_response").get("code") != 0:
            #     address.decrease_sequence()
            #     raise TxError(tx_output.raw_log)
            #
            # tx_output["rawLog"] = json.loads(tx_output.get("rawLog", "{}"))
            # return pt.RawSyncTxResp(tx_output)
        except exceptions.ErrorQueryTx as err:
            logging.info("ErrorQueryTx")
            logging.error(err)
            raise err
        except BaseException as err:
            logging.info("BaseException")
            logging.error(err)
            raise err

    def execute_tx(
        self,
        tx: "Transaction",
        gas_estimate: float,
        use_tmrpc: bool = True,
        tx_config: Optional[pt.TxConfig] = None,
    ) -> Union[jsonrpc.JsonRPCResponse, abci_type.TxResponse]:
        conf: pt.TxConfig = self.ensure_tx_config(new_tx_config=tx_config)

        def compute_gas_wanted() -> float:
            # Related to https://github.com/cosmos/cosmos-sdk/issues/14405
            # TODO We should consider adding the behavior mentioned by tac0turtle.
            gas_wanted = gas_estimate * 1.25  # apply gas multiplier
            if conf.gas_wanted > 0:
                gas_wanted = conf.gas_wanted
            elif conf.gas_multiplier > 0:
                gas_wanted = gas_estimate * conf.gas_multiplier
            return gas_wanted

        gas_wanted = compute_gas_wanted()
        gas_price = pt.DEFAULT_GAS_PRICE if conf.gas_price <= 0 else conf.gas_price

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
            tx.with_gas_limit(gas_wanted)
            .with_fee(fee)
            .with_memo("")
            .with_timeout_height(self.client.timeout_height)
        )
        tx_raw_bytes: bytes = tx.get_signed_tx_data()

        if use_tmrpc:
            return self._broadcast_tx_jsonrpc(
                tx_raw_bytes=tx_raw_bytes,
            )
        else:
            return self._broadcast_tx_grpc(
                tx_raw_bytes=tx_raw_bytes, tx_type=conf.broadcast_mode
            )

    def _broadcast_tx_jsonrpc(
        self,
        tx_raw_bytes: bytes,
        tx_type: pt.TxBroadcastMode = pt.TxBroadcastMode.SYNC,
    ) -> jsonrpc.jsonrpc.JsonRPCResponse:
        jsonrpc_req: jsonrpc.JsonRPCRequest = tmrpc.BroadcastTxSync.create(
            tx_raw_bytes=tx_raw_bytes,
            id=420,
        )
        return jsonrpc.jsonrpc.do_jsonrpc_request(
            data=jsonrpc_req, endpoint=self.network.tendermint_rpc_endpoint
        )

    def _broadcast_tx_grpc(
        self,
        tx_raw_bytes: bytes,
        tx_type: pt.TxBroadcastMode = pt.TxBroadcastMode.SYNC,
    ) -> abci_type.TxResponse:
        """Broadcast the signed transaction to one or more nodes in the
        network. The nodes in the network will receive the transaction
        and validate its integrity by verifying the signature, checking
        if the sender has sufficient funds or permissions, and running
        the `ValidateBasic` check on each tx message.

        Args:
            tx_raw_bytes (bytes): Signed transaction.
            tx_type (pt.TxBroadcastMode): Broadcast mode for the transaction

        Returns:
            (abci_type.TxResponse)
        """

        broadcast_mode: tx_service.Broadcast
        if tx_type == pt.TxBroadcastMode.ASYNC:
            broadcast_mode = tx_service.BroadcastMode.BROADCAST_MODE_ASYNC
        else:
            broadcast_mode = tx_service.BroadcastMode.BROADCAST_MODE_SYNC
        return self.client.broadcast_tx(
            tx_byte=tx_raw_bytes,
            mode=broadcast_mode,
        )

    def build_tx_with_node_sequence(
        self,
        msgs: Union[pt.PythonMsg, List[pt.PythonMsg]],
    ):
        address: wallet.Address = self.ensure_address_info()
        sequence: int = address.get_sequence(
            from_node=True,
            lcd_endpoint=self.network.lcd_endpoint,
        )
        return self.build_tx(msgs=msgs, sequence=sequence)

    def build_tx(
        self,
        msgs: Union[pt.PythonMsg, List[pt.PythonMsg]],
        sequence: Optional[int] = None,
    ) -> Tuple["Transaction", wallet.Address]:
        if not isinstance(msgs, list):
            msgs = [msgs]

        pb_msgs = [msg.to_pb() for msg in msgs]
        self.client.sync_timeout_height()

        address: wallet.Address
        if self.address is None:
            address = self.ensure_address_info()
            self.address = address
        else:
            assert isinstance(self.address, wallet.Address)
            address = self.address

        if sequence is None:
            sequence = self.address.sequence

        tx = (
            Transaction()
            .with_messages(pb_msgs)
            .with_sequence(sequence)
            .with_account_num(address.get_number())
            .with_chain_id(self.network.chain_id)
            .with_signer(self.priv_key)
        )
        return tx, address

    def simulate(self, tx: "Transaction") -> abci_type.SimulationResponse:
        """
        Args:
            tx (Transaction): The transaction being simulated.

        Returns:
            SimulationResponse: SimulationResponse defines the response
                generated when a transaction is simulated successfully.

        Raises:
            SimulationError
        """
        sim_tx_raw_bytes: bytes = tx.get_signed_tx_data()

        sim_res: abci_type.SimulationResponse
        success: bool
        sim_res, success = self.client.simulate_tx(sim_tx_raw_bytes)
        if not success:
            raise SimulationError(sim_res)

        return sim_res

    def ensure_address_info(self) -> wallet.Address:
        """Guarantees that the TxClient.address has been set and returns it.
        If the wallet address has not been set prior to this function call,
        (1) the address is derived from the 'priv_key' and
        (2) the sequence is derived from the 'network.lcd_endpoint'.
        """
        if self.address is None:
            pub_key: wallet.PublicKey = self.priv_key.to_public_key()
            self.address = pub_key.to_address()
            self.address = self.address.init_num_seq(self.network.lcd_endpoint)

        return self.address

    def ensure_tx_config(
        self,
        new_tx_config: pt.TxConfig = None,
    ) -> pt.TxConfig:
        """Guarantees that the TxClient.tx_config has been set and returns it.

        Args:
            new_tx_config (Optional[pytypes.TxConfig]): Becomes the new value
                for the tx config if given. Defaults to None.

        Returns:
            (pt.TxConfig): The new value for the TxClient.tx_config.
        """
        tx_config: pt.TxConfig
        if new_tx_config is not None:
            tx_config = new_tx_config
        elif self.tx_config is None:
            # Set as the default if the TxConfig has not been initialized.
            tx_config = pt.TxConfig()
        else:
            pass
        tx_config = self.tx_config
        return tx_config


# TODO: Refactor this into a dataclass for brevity.
class Transaction(pt.Jsonable):
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
        sequence (int): A per sender "nonce" that acts as a security measure to
            prevent replay attacks on transactions. Each transaction request must
            have a different sequence number from all previously executed
            transactions so that no transaction can be replayed.
        chain_id (str): The unique identifier for the blockchain that this
            transaction targets. Inclusion of a 'chain_id' prevents potential
            attackers from using signed transactions on other blockchains.
        fee (List[Coin]): Coins to be paid in fees. The 'fee' helps prevents end
            users from spamming the network. Gas cosumed during message execution
            is typically priced from a fee equal to 'gas_consumed * gas_prices'.
            Here, 'gas_prices' is the minimum gas price, and it's a parameter local
            to each node.
        gas_limit (int): Maximum gas to be allowed for the transaction. The
            transaction execution fails if the gas limit is exceeded.
        priv_key (wallet.PrivateKey): Primary signer for the transaction. By
            convention, the signer from the first message is referred to as the
            primary signer and pays the fee for the whole transaction. We refer
            to this primary signer with 'priv_key'.
        memo (str): Memo is a note or comment to be added to the transaction.
        timeout_height (int): Timeout height is the block height after which
            the transaction will not be processed by the chain.
    """

    def __init__(
        self,
        msgs: Tuple[message.Message, ...] = None,
        account_num: int = None,
        priv_key: wallet.PrivateKey = None,
        sequence: int = None,
        chain_id: str = None,
        fee: List[Coin] = None,
        gas_limit: int = 0,
        memo: str = "",
        timeout_height: int = 0,
    ):
        self.msgs = self.__convert_msgs(msgs) if msgs is not None else []
        self.account_num = account_num
        self.priv_key = priv_key
        self.sequence = sequence
        self.chain_id = chain_id
        self.fee = cosmos_tx_type.Fee(amount=fee, gas_limit=gas_limit)
        self.gas_limit = gas_limit
        self.memo = memo
        self.timeout_height = timeout_height

    def __repr__(self) -> str:
        self_as_dict = dict(
            msgs=[self.msgs],
            sequence=self.sequence,
            account_num=self.account_num,
            chain_id=self.chain_id,
            fee=self.fee,
            gas_limit=self.gas_limit,
            memo=self.memo,
            timeout_height=self.timeout_height,
            priv_key=self.priv_key,
        )
        return pprint.pformat(self_as_dict, indent=2)

    @property
    def raw_bytes(self) -> bytes:
        return self.get_signed_tx_data()

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

    def with_gas_limit(self, gas: Number) -> "Transaction":
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
            raise ValueError("no messages in the tx body")

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
        return self.get_tx_data(signature=sig, public_key=pub_key)
