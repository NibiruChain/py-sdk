Module nibiru.grpc_client
=========================

Classes
-------

`GrpcClient(network: nibiru.network.Network, insecure=False, credentials: grpc.ChannelCredentials = None, bypass_version_check: bool = False)`
:   _summary_

    Args:
        network (Network): The network object
        insecure (bool, optional): Wether the network should use ssl or not. Defaults to False.
        credentials (grpc.ChannelCredentials, optional): Ssl creds. Defaults to None.
        bypass_version_check (bool, optional): Wether to bypass the check for correct version of the chain/py-sdk

    ### Static methods

    `assert_compatible_versions(nibiru_proto_version, chain_nibiru_version)`
    :   Assert that this version of the python sdk is compatible with the chain.
        If you run the chain from a non tagged release, the version query will be returning something like
        master-6a315bab3db46f5fa1158199acc166ed2d192c2f. Otherwise, it should be for example `v0.14.0`.

        If the chain is running a custom non tagged release, you are free to use the python sdk at your own risk.

    ### Methods

    `close_chain_channel(self)`
    :

    `get_account(self, address: str) ‑> Optional[cosmos.auth.v1beta1.auth_pb2.BaseAccount]`
    :   Returns the account info from address

        Args:
            address: the address of the account

        Returns:
            Optional[auth_type.BaseAccount]: the account information, none if not found

    `get_bank_balance(self, address: str, denom: str)`
    :   Gets the balance of asset denom of an account

        Args:
            address: the account address
            denom: the denom

    `get_bank_balances(self, address: str)`
    :   Get all balances from an account

        Args:
            address: the account address

    `get_block_by_height(self, height: int) ‑> cosmos.base.tendermint.v1beta1.query_pb2.GetBlockByHeightResponse`
    :   Returns the block specified by height

        Args:
            height: the height of the block

        Returns:
            tendermint_query.GetBlockByHeightResponse: the block info

    `get_blocks_by_height(self, start_height: int, end_height: int = None) ‑> Generator[cosmos.base.tendermint.v1beta1.query_pb2.GetBlockByHeightResponse, None, None]`
    :   Iterate through all the blocks in the chain and yield the output of the block one by one.
        If no end_height is specified, iterate until the current latest block is reached.

        Args:
            start_height (int): The starting block height
            end_height (int, optional): The last block height to query. Defaults to None.

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

    `send_tx_async_mode(self, tx_byte: bytes) ‑> cosmos.base.abci.v1beta1.abci_pb2.TxResponse`
    :   Sends a transaction in async mode

        Args:
            tx_byte: the tx in bytes

        Returns:
            abci_type.TxResponse: the tx response

    `send_tx_block_mode(self, tx_byte: bytes) ‑> cosmos.base.abci.v1beta1.abci_pb2.TxResponse`
    :   Sends a transaction in block mode

        Args:
            tx_byte: the tx in bytes

        Returns:
            abci_type.TxResponse: the tx response

    `send_tx_sync_mode(self, tx_byte: bytes) ‑> cosmos.base.abci.v1beta1.abci_pb2.TxResponse`
    :   Sends a transaction in sync mode

        Args:
            tx_byte: the tx in bytes

        Returns:
            abci_type.TxResponse: the tx response

    `simulate_tx(self, tx_byte: bytes) ‑> Tuple[Union[cosmos.base.abci.v1beta1.abci_pb2.SimulationResponse, grpc.RpcError], bool]`
    :

    `sync_timeout_height(self)`
    :

    `wait_for_next_block(self)`
    :   Wait for a block to be written
