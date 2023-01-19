import logging
import time
from typing import Generator, List, Optional, Tuple, Union

import grpc
import nibiru_proto.cosmos.auth.v1beta1 as auth
import nibiru_proto.cosmos.authz.v1beta1 as authz
import nibiru_proto.cosmos.bank.v1beta1 as bank
import nibiru_proto.cosmos.base.abci.v1beta1 as abci_type
import nibiru_proto.cosmos.base.tendermint.v1beta1 as tendermint
import nibiru_proto.cosmos.tx.v1beta1 as pb_tx
from packaging import version

from nibiru import pytypes, query_clients

DEFAULT_TIMEOUTHEIGHT = 20  # blocks
GITHUB_COMMIT_HASH_LEN = 40


class GrpcClient:
    def __init__(
        self,
        network: pytypes.Network,
        insecure=False,
        credentials: grpc.ChannelCredentials = None,
        bypass_version_check: bool = False,
    ):
        """
        _summary_

        Args:
            network (Network): The network object
            insecure (bool, optional): Wether the network should use ssl or not. Defaults to False.
            credentials (grpc.ChannelCredentials, optional): Ssl creds. Defaults to None.
            bypass_version_check (bool, optional): Wether to bypass the check for correct version of the chain/py-sdk
        """

        # load root CA cert
        if not insecure:
            credentials = grpc.ssl_channel_credentials()

        # chain stubs
        grpc_endpoint = network.grpc_endpoint.lstrip("tcp://")
        self.chain_channel = (
            grpc.insecure_channel(grpc_endpoint)
            if insecure
            else grpc.secure_channel(grpc_endpoint, credentials)
        )

        self.stubCosmosTendermint = tendermint.ServiceStub(self.chain_channel)
        self.stubAuth = auth.QueryStub(self.chain_channel)
        self.stubAuthz = authz.QueryStub(self.chain_channel)
        self.stubBank = bank.QueryStub(self.chain_channel)
        self.stubTx = pb_tx.ServiceStub(self.chain_channel)

        self.timeout_height = 1

        # Query services
        self.dex = query_clients.DexQueryClient(self.chain_channel)
        self.perp = query_clients.PerpQueryClient(self.chain_channel)
        self.vpool = query_clients.VpoolQueryClient(self.chain_channel)
        self.epoch = query_clients.EpochQueryClient(self.chain_channel)
        self.auth = query_clients.AuthQueryClient(self.chain_channel)
        self.staking = query_clients.StakingQueryClient(self.chain_channel)

        if not bypass_version_check:
            try:
                from importlib import metadata
            except ImportError:  # for Python<3.8
                import importlib_metadata as metadata

            nibiru_proto_version = metadata.version("nibiru_proto")

            self.assert_compatible_versions(
                nibiru_proto_version=nibiru_proto_version,
                chain_nibiru_version=str(self.get_version()),
            )

    @staticmethod
    def assert_compatible_versions(nibiru_proto_version, chain_nibiru_version):
        """
        Assert that this version of the python sdk is compatible with the chain.
        If you run the chain from a non tagged release, the version query will be returning something like
        master-6a315bab3db46f5fa1158199acc166ed2d192c2f. Otherwise, it should be for example `v0.14.0`.

        If the chain is running a custom non tagged release, you are free to use the python sdk at your own risk.
        """
        if nibiru_proto_version[0] == "v":
            nibiru_proto_version = nibiru_proto_version[1:]
        if chain_nibiru_version[0] == "v":
            chain_nibiru_version = chain_nibiru_version[1:]

        if len(chain_nibiru_version) >= GITHUB_COMMIT_HASH_LEN:
            logger = logging.getLogger("client-logger")
            logger.warning(
                f"The chain is running a custom release from branch/commit {chain_nibiru_version}. "
                "We bypass the compatibility assertion"
            )
            logger.warning(
                f"The chain is running a custom release from branch/commit {chain_nibiru_version}"
            )
        else:

            error_string = (
                f"Version error, Python sdk runs with nibiru protobuf version {nibiru_proto_version}, but the "
                f"remote chain is running with version {chain_nibiru_version}"
            )

            assert (
                version.parse(nibiru_proto_version).major
                >= version.parse(chain_nibiru_version).major
            ) and (
                version.parse(nibiru_proto_version).minor
                >= version.parse(chain_nibiru_version).minor
            ), error_string

    def close_chain_channel(self):
        self.chain_channel.close()

    def sync_timeout_height(self):
        block = self.get_latest_block()
        self.timeout_height = block.block.header.height + DEFAULT_TIMEOUTHEIGHT

    def wait_for_next_block(self):
        """
        Wait for a block to be written
        """
        current_block = self.get_latest_block().block.header.height
        while self.get_latest_block().block.header.height < current_block + 1:
            time.sleep(0.5)

    def get_block_by_height(self, height: int) -> tendermint.GetBlockByHeightResponse:
        """
        Returns the block specified by height

        Args:
            height: the height of the block

        Returns:
            tendermint.GetBlockByHeightResponse: the block info

        """
        req = tendermint.GetBlockByHeightRequest(height=height)
        return self.stubCosmosTendermint.get_block_by_height(req)

    def get_blocks_by_height(
        self, start_height: int, end_height: int = None
    ) -> Generator[tendermint.GetBlockByHeightResponse, None, None]:
        """
        Iterate through all the blocks in the chain and yield the output of the block one by one.
        If no end_height is specified, iterate until the current latest block is reached.

        Args:
            start_height (int): The starting block height
            end_height (int, optional): The last block height to query. Defaults to None.

        Yields:
            Generator[tendermint.GetBlockByHeightResponse, None, None]
        """
        if end_height is None:
            height = start_height
            while True:
                try:
                    yield self.get_block_by_height(height)
                    height += 1
                except:
                    break
        else:
            for height in range(start_height, end_height):
                yield self.get_block_by_height(height)

    # default client methods
    def get_latest_block(self) -> tendermint.GetLatestBlockResponse:
        """
        Returns the last block

        Returns:
            tendermint.GetLatestBlockResponse: the last block information

        """
        req = tendermint.GetLatestBlockRequest()
        return self.stubCosmosTendermint.get_latest_block(req)

    def get_version(self) -> str:
        """
        Returns the application version

        Returns:
            str: the version of the app

        """
        req = tendermint.GetNodeInfoRequest()
        version = self.stubCosmosTendermint.get_node_info(
            req
        ).application_version.version

        if version[0] != "v":
            version = "v" + str(version)

        return version

    def get_latest_block_height(self) -> int:
        """
        Returns the latest block height

        Returns:
            int: the last block height

        """
        return self.get_latest_block().block.header.height

    def get_account(self, address: str) -> Optional[auth.BaseAccount]:
        """
        Returns the account info from address

        Args:
            address: the address of the account

        Returns:
            Optional[auth.BaseAccount]: the account information, none if not found

        """
        try:
            account_any = self.stubAuth.account(
                auth.QueryAccountRequest(address=address)
            ).account
            account = auth.BaseAccount()
            if account_any.Is(account.DESCRIPTOR):
                account_any.Unpack(account)
                return account
        except:
            return None

    def get_request_id_by_tx_hash(self, tx_hash: bytes) -> List[int]:
        tx = self.stubTx.get_tx(pb_tx.GetTxRequest(hash=tx_hash))
        request_ids = []
        for tx in tx.tx_response.logs:
            request_event = [
                event
                for event in tx.events
                if event.type == "request" or event.type == "report"
            ]
            if len(request_event) == 1:
                attrs = request_event[0].attributes
                attr_id = [attr for attr in attrs if attr.key == "id"]
                if len(attr_id) == 1:
                    request_id = attr_id[0].value
                    request_ids.append(int(request_id))
        if len(request_ids) == 0:
            raise KeyError("Request Id is not found")
        return request_ids

    def simulate_tx(
        self, tx_byte: bytes
    ) -> Tuple[Union[abci_type.SimulationResponse, grpc.RpcError], bool]:
        try:
            req = pb_tx.SimulateRequest(tx_bytes=tx_byte)
            return self.stubTx.simulate.__call__(req), True
        except grpc.RpcError as err:
            return err._state.details, False

    def send_tx_sync_mode(self, tx_byte: bytes) -> abci_type.TxResponse:
        """
        Sends a transaction in sync mode

        Args:
            tx_byte: the tx in bytes

        Returns:
            abci_type.TxResponse: the tx response

        """
        req = pb_tx.BroadcastTxRequest(
            tx_bytes=tx_byte, mode=pb_tx.BroadcastMode.BROADCAST_MODE_SYNC
        )
        result = self.stubTx.broadcast_tx.__call__(req)
        return result.tx_response

    def send_tx_async_mode(self, tx_byte: bytes) -> abci_type.TxResponse:
        """
        Sends a transaction in async mode

        Args:
            tx_byte: the tx in bytes

        Returns:
            abci_type.TxResponse: the tx response

        """
        req = pb_tx.BroadcastTxRequest(
            tx_bytes=tx_byte, mode=pb_tx.BroadcastMode.BROADCAST_MODE_ASYNC
        )
        result = self.stubTx.broadcast_tx.__call__(req)
        return result.tx_response

    def send_tx_block_mode(self, tx_byte: bytes) -> abci_type.TxResponse:
        """
        Sends a transaction in block mode

        Args:
            tx_byte: the tx in bytes

        Returns:
            abci_type.TxResponse: the tx response

        """
        req = pb_tx.BroadcastTxRequest(
            tx_bytes=tx_byte, mode=pb_tx.BroadcastMode.BROADCAST_MODE_BLOCK
        )
        result = self.stubTx.broadcast_tx.__call__(req)
        return result.tx_response

    def get_chain_id(self) -> str:
        """
        Gets the chain id

        Returns:
            str: the chain id

        """
        latest_block = self.get_latest_block()
        return latest_block.block.header.chain_id

    def get_grants(self, granter: str, grantee: str, **kwargs):
        return self.stubAuthz.grants(
            authz.QueryGrantsRequest(
                granter=granter,
                grantee=grantee,
                msg_type_url=kwargs.get("msg_type_url"),
            )
        )

    def get_bank_balances(self, address: str) -> dict:
        """
        Returns the balances of all coins for the given 'address'

        Args:
            address: the account address

        Returns
            dict: balances for each coin
        """
        return query_clients.deserialize(
            self.stubBank.all_balances(bank.QueryAllBalancesRequest(address=address))
        )

    def get_bank_balance(self, address: str, denom: str) -> dict:
        """
        Returns the balance of 'denom' for the given 'address'

        Args:
            address: the account address
            denom: the denom

        Returns:
            dict: balance for the coin with denom, 'denom'
        """
        return query_clients.deserialize(
            self.stubBank.balance(
                bank.QueryBalanceRequest(address=address, denom=denom)
            )
        )
