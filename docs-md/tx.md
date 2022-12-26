Module nibiru.tx
================
Classes:
    TxClient: A client for building, simulating, and broadcasting transactions.
    Transaction: Transactions trigger state changes based on messages. Each message
        must be cryptographically signed before being broadcasted to the network.

Classes
-------

`Transaction(msgs: Tuple[google.protobuf.message.Message, ...] = None, account_num: int = None, priv_key: nibiru.wallet.PrivateKey = None, sequence: int = None, chain_id: str = None, fee: List[cosmos.base.v1beta1.coin_pb2.Coin] = None, gas_limit: int = 0, memo: str = '', timeout_height: int = 0)`
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

    `with_gas_limit(self, gas: numbers.Number) ‑> nibiru.tx.Transaction`
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
:   A client for building, simulating, and broadcasting transactions.

    ### Methods

    `build_tx(self, msgs: Union[nibiru.pytypes.common.PythonMsg, List[nibiru.pytypes.common.PythonMsg]], get_sequence_from_node: bool = False) ‑> Tuple[nibiru.tx.Transaction, nibiru.wallet.Address]`
    :

    `execute_msgs(self, msgs: Union[nibiru.pytypes.common.PythonMsg, List[nibiru.pytypes.common.PythonMsg]], get_sequence_from_node: bool = False, **kwargs) ‑> nibiru.pytypes.tx_resp.RawTxResp`
    :   Broadcasts messages to a node in a single transaction. This function first
        simulates the corresponding transaction to estimate the amount of gas needed.

        If the transaction fails because of account sequence mismatch, we try to
        query the sequence from the LCD endpoint and broadcast with the updated
        sequence value.

        Args:
            get_sequence_from_node (bool, optional): Specifies whether the sequence
                comes from the local value or the lcd endpoint. Defaults to False.

        Raises:
            SimulationError: If broadcasting fails during the simulation.
            TxError: If the response code is nonzero, the 'TxError' includes the
                raw error logs from the blockchain.

        Returns:
            Union[RawTxResp, Dict[str, Any]]: The transaction response as a dict
                in proto3 JSON format.

    `execute_tx(self, tx: Transaction, gas_estimate: float, **kwargs) ‑> cosmos.base.abci.v1beta1.abci_pb2.TxResponse`
    :

    `get_address_info(self) ‑> nibiru.wallet.Address`
    :

    `get_config(self, **kwargs) ‑> nibiru.pytypes.common.TxConfig`
    :   Properties in kwargs overwrite the self.config

    `simulate(self, tx: Transaction) ‑> cosmos.base.abci.v1beta1.abci_pb2.SimulationResponse`
    :   Args:
            tx (Transaction): The transaction being simulated.

        Returns:
            SimulationResponse: SimulationResponse defines the response generated
                when a transaction is simulated successfully.

        Raises:
            SimulationError
