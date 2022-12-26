Module nibiru.tx
================
Classes:
    TxClient
    Transaction

Classes
-------

`Transaction(msgs: Tuple[google.protobuf.message.Message, ...] = None, account_num: int = None, priv_key: nibiru.wallet.PrivateKey = None, sequence: int = None, chain_id: str = None, fee: List[cosmos.base.v1beta1.coin_pb2.Coin] = None, gas: int = 0, memo: str = '', timeout_height: int = 0)`
:   Transactions trigger state changes based on messages ('msgs'). Each message
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

    ### Methods

    `get_sign_doc(self, public_key: nibiru.wallet.PublicKey = None) ‑> cosmos.tx.v1beta1.tx_pb2.SignDoc`
    :

    `get_signed_tx_data(self) ‑> bytes`
    :

    `get_tx_data(self, signature: bytes, public_key: nibiru.wallet.PublicKey = None) ‑> bytes`
    :

    `with_account_num(self, account_num: int) ‑> nibiru.tx.Transaction`
    :

    `with_chain_id(self, chain_id: str) ‑> nibiru.tx.Transaction`
    :

    `with_fee(self, fee: List[cosmos.base.v1beta1.coin_pb2.Coin]) ‑> nibiru.tx.Transaction`
    :

    `with_gas(self, gas: numbers.Number) ‑> nibiru.tx.Transaction`
    :

    `with_memo(self, memo: str) ‑> nibiru.tx.Transaction`
    :

    `with_messages(self, msgs: Iterable[google.protobuf.message.Message]) ‑> nibiru.tx.Transaction`
    :

    `with_sender(self, client: nibiru.grpc_client.GrpcClient, sender: str) ‑> nibiru.tx.Transaction`
    :

    `with_sequence(self, sequence: int) ‑> nibiru.tx.Transaction`
    :

    `with_signer(self, priv_key: nibiru.wallet.PrivateKey)`
    :

    `with_timeout_height(self, timeout_height: int) ‑> nibiru.tx.Transaction`
    :

`TxClient(priv_key: nibiru.wallet.PrivateKey, network: nibiru.pytypes.network.Network, client: nibiru.grpc_client.GrpcClient, config: nibiru.pytypes.common.TxConfig)`
:

    ### Methods

    `execute_msgs(self, msgs: Union[nibiru.pytypes.common.PythonMsg, List[nibiru.pytypes.common.PythonMsg]], get_sequence_from_node: bool = False, **kwargs) ‑> nibiru.pytypes.tx_resp.RawTxResp`
    :   Execute a message to broadcast a transaction to the node.
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

    `execute_tx(self, tx: Transaction, gas_estimate: float, **kwargs) ‑> cosmos.base.abci.v1beta1.abci_pb2.TxResponse`
    :

    `get_address_info(self)`
    :

    `get_config(self, **kwargs) ‑> nibiru.pytypes.common.TxConfig`
    :   Properties in kwargs overwrite config

    `simulate(self, tx: Transaction)`
    :
