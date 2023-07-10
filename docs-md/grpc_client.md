Module pysdk.grpc_client
========================

Classes
-------

`GrpcClient(network: pysdk.pytypes.network.Network, insecure=False, credentials: grpc.ChannelCredentials = None, bypass_version_check: bool = False)`
:   gRPC client for Nibiru implemented in Python.

    Args and Attributes:
        network (Network): The network object
        insecure (bool, optional): Wether the network should use ssl or
            not. Defaults to False.
        credentials (grpc.ChannelCredentials, optional): Ssl creds.
            Defaults to None.
        bypass_version_check (bool, optional): Wether to bypass the check
            for correct version of the chain/py-sdk.

    Background:

    gRPC is a high-performance, open-source universal remote procedure call
    (RPC) framework developed by Google. The main purpose of gRPC is to allow a
    program or application in one device to make requests to a service in
    another device, which could be located in a different network, as if it
    were a local object.

    This is done through a process called serialization, where data structures
    are translated into a format that can be stored and reconstructed later.
    gRPC is language-agnostic, meaning it can be used with numerous programming
    languages, making it highly versatile.

    gRPC uses Protocol Buffers as its interface definition language, enabling
    the definition of services and message types, which are then compiled to
    generate client and server side code. Its key features include low latency,
    high scalability, and strong security, making it well-suited for connecting
    services in distributed systems.

    ### Static methods

    `assert_compatible_versions(nibiru_proto_version, chain_nibiru_version)`
    :   Assert that this version of the python sdk is compatible with the chain.
        If you run the chain from a non tagged release, the version query will
        return something like:
        master-6a315bab3db46f5fa1158199acc166ed2d192c2f.

        Otherwise, it should be a semver string of the form
        `v[major].[minor].[patch]` like `v0.14.0`.

        If the chain is running a custom non tagged release, please use the
        Python SDK at your own risk, as it can still sign and broadcast
        transactions, but you'll have no guarantees on the resulting state
        changes in the blockchain.

    ### Methods

    `broadcast_tx(self, tx_byte: bytes, mode: <google.protobuf.internal.enum_type_wrapper.EnumTypeWrapper object at 0x7f49911fa610> = 2) ‑> cosmos.base.abci.v1beta1.abci_pb2.TxResponse`
    :   Broadcast the signed transaction to one or more nodes in the
        network. The nodes in the network will receive the transaction
        and validate its integrity by verifying the signature, checking
        if the sender has sufficient funds or permissions, and running
        the `ValidateBasic` check on each tx message.

        Args:
            tx_raw_bytes (bytes): Signed transaction.
            tx_type (pt.TxBroadcastMode): Broadcast mode for the transaction

        Returns:
            (abci_type.TxResponse)

    `close_chain_channel(self)`
    :

    `get_account(self, address: str) ‑> Optional[cosmos.auth.v1beta1.auth_pb2.BaseAccount]`
    :   Returns the account info from address

        Args:
            address: the address of the account

        Returns:
            Optional[auth_type.BaseAccount]: the account information, none if not found

    `get_bank_balance(self, address: str, denom: str) ‑> dict`
    :   Returns the balance of 'denom' for the given 'address'
        Args:
            address: the account address
            denom: the denom

        Returns:
            dict: balance for the coin with denom, 'denom'

    `get_bank_balances(self, address: str) ‑> Dict[str, List[Dict[Literal['denom', 'amount'], Union[str, int]]]]`
    :   Returns the balances of all coins for the given 'address'

        Args:
            address: the account address

        Returns
            dict: balances for each coin

    `get_block_by_height(self, height: int) ‑> cosmos.base.tendermint.v1beta1.query_pb2.GetBlockByHeightResponse`
    :   Returns the block specified by height

        Args:
            height: the height of the block

        Returns:
            tendermint_query.GetBlockByHeightResponse: the block info

    `get_blocks_by_height(self, start_height: int, end_height: int = None) ‑> Generator[cosmos.base.tendermint.v1beta1.query_pb2.GetBlockByHeightResponse, None, None]`
    :   Iterate through all the blocks in the chain and yield the output of the
        block one by one. If no end_height is specified, iterate until the
        current latest block is reached.

        Args:
            start_height (int): The starting block height
            end_height (int, optional): The last block height to query.
                Defaults to None.

        Yields:
            Generator[tendermint_query.GetBlockByHeightResponse, None, None]

    `get_chain_id(self) ‑> str`
    :   Gets the chain id

        Returns:
            str: the chain id

    `get_grants(self, granter: str, grantee: str, **kwargs)`
    :

    `get_latest_block(self) ‑> cosmos.base.tendermint.v1beta1.query_pb2.GetLatestBlockResponse`
    :   Returns the last block

        Returns:
            tendermint_query.GetLatestBlockResponse: the last block information

    `get_latest_block_height(self) ‑> int`
    :   Returns the latest block height

        Returns:
            int: the last block height

    `get_request_id_by_tx_hash(self, tx_hash: bytes) ‑> List[int]`
    :

    `get_version(self) ‑> str`
    :   Returns the application version

        Returns:
            str: the version of the app

    `simulate_tx(self, tx_byte: bytes) ‑> Tuple[Union[cosmos.base.abci.v1beta1.abci_pb2.SimulationResponse, grpc.RpcError], bool]`
    :

    `sync_timeout_height(self)`
    :

    `tx_by_hash(self, tx_hash: str) ‑> cosmos.tx.v1beta1.service_pb2.GetTxResponse`
    :   Fetches a tx by hash

    `wait_for_next_block(self)`
    :   Wait for a block to be written
