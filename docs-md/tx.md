Module pysdk.tx
===============
Classes:
    TxClient: A client for building, simulating, and broadcasting transactions.
    Transaction: Transactions trigger state changes based on messages. Each
        message must be cryptographically signed before being broadcasted to
        the network.

Classes
-------

`Transaction(msgs: Tuple[google.protobuf.message.Message, ...] = None, account_num: int = None, priv_key: pysdk.wallet.PrivateKey = None, sequence: int = None, chain_id: str = None, fee: List[cosmos.base.v1beta1.coin_pb2.Coin] = None, gas_limit: int = 0, memo: str = '', timeout_height: int = 0)`
:   Transactions trigger state changes based on messages ('msgs'). Each message
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

    ### Ancestors (in MRO)

    * pysdk.pytypes.jsonable.Jsonable
    * abc.ABC

    ### Instance variables

    `raw_bytes: bytes`
    :

    ### Methods

    `get_sign_doc(self, public_key: pysdk.wallet.PublicKey = None) ‑> cosmos.tx.v1beta1.tx_pb2.SignDoc`
    :

    `get_signed_tx_data(self) ‑> bytes`
    :

    `get_tx_data(self, signature: bytes, public_key: pysdk.wallet.PublicKey = None) ‑> bytes`
    :

    `with_account_num(self, account_num: int) ‑> pysdk.tx.Transaction`
    :

    `with_chain_id(self, chain_id: str) ‑> pysdk.tx.Transaction`
    :

    `with_fee(self, fee: List[cosmos.base.v1beta1.coin_pb2.Coin]) ‑> pysdk.tx.Transaction`
    :

    `with_gas_limit(self, gas: numbers.Number) ‑> pysdk.tx.Transaction`
    :

    `with_memo(self, memo: str) ‑> pysdk.tx.Transaction`
    :

    `with_messages(self, msgs: Iterable[google.protobuf.message.Message]) ‑> pysdk.tx.Transaction`
    :

    `with_sender(self, client: pysdk.grpc_client.GrpcClient, sender: str) ‑> pysdk.tx.Transaction`
    :

    `with_sequence(self, sequence: int) ‑> pysdk.tx.Transaction`
    :

    `with_signer(self, priv_key: pysdk.wallet.PrivateKey)`
    :

    `with_timeout_height(self, timeout_height: int) ‑> pysdk.tx.Transaction`
    :

`TxClient(priv_key: pysdk.wallet.PrivateKey, network: pysdk.pytypes.network.Network, client: pysdk.grpc_client.GrpcClient, config: pysdk.pytypes.common.TxConfig)`
:   A client for building, simulating, and broadcasting transactions.

    Attributes:
        address (Optional[wallet.Address])
        client (GrpcClient)
        network (pt.Network)
        priv_key (wallet.PrivateKey)
        tx_config (pt.TxConfig)

    ### Class variables

    `address: Optional[pysdk.wallet.Address]`
    :

    `client: pysdk.grpc_client.GrpcClient`
    :

    `network: pysdk.pytypes.network.Network`
    :

    `priv_key: pysdk.wallet.PrivateKey`
    :

    `tx_config: pysdk.pytypes.common.TxConfig`
    :

    ### Methods

    `build_tx(self, msgs: Union[pysdk.pytypes.common.PythonMsg, List[pysdk.pytypes.common.PythonMsg]], sequence: Optional[int] = None) ‑> Tuple[pysdk.tx.Transaction, pysdk.wallet.Address]`
    :

    `build_tx_with_node_sequence(self, msgs: Union[pysdk.pytypes.common.PythonMsg, List[pysdk.pytypes.common.PythonMsg]])`
    :

    `ensure_address_info(self) ‑> pysdk.wallet.Address`
    :   Guarantees that the TxClient.address has been set and returns it.
        If the wallet address has not been set prior to this function call,
        (1) the address is derived from the 'priv_key' and
        (2) the sequence is derived from the 'network.lcd_endpoint'.

    `ensure_tx_config(self, new_tx_config: pysdk.pytypes.common.TxConfig = None) ‑> pysdk.pytypes.common.TxConfig`
    :   Guarantees that the TxClient.tx_config has been set and returns it.

        Args:
            new_tx_config (Optional[pytypes.TxConfig]): Becomes the new value
                for the tx config if given. Defaults to None.

        Returns:
            (pt.TxConfig): The new value for the TxClient.tx_config.

    `execute_msgs(self, msgs: Union[pysdk.pytypes.common.PythonMsg, List[pysdk.pytypes.common.PythonMsg]], sequence: Optional[int] = None, tx_config: Optional[pysdk.pytypes.common.TxConfig] = None) ‑> pysdk.pytypes.tx_resp.ExecuteTxResp`
    :   Broadcasts messages to a node in a single transaction. This function
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

    `execute_tx(self, tx: Transaction, gas_estimate: float, use_tmrpc: bool = True, tx_config: Optional[pysdk.pytypes.common.TxConfig] = None) ‑> Union[pysdk.jsonrpc.jsonrpc.JsonRPCResponse, cosmos.base.abci.v1beta1.abci_pb2.TxResponse]`
    :

    `simulate(self, tx: Transaction) ‑> cosmos.base.abci.v1beta1.abci_pb2.SimulationResponse`
    :   Args:
            tx (Transaction): The transaction being simulated.

        Returns:
            SimulationResponse: SimulationResponse defines the response
                generated when a transaction is simulated successfully.

        Raises:
            SimulationError
