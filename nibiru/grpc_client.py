import logging
import time
from typing import Generator, List, Optional, Tuple, Union

import grpc
from nibiru_proto.proto.cosmos.auth.v1beta1 import auth_pb2 as auth_type
from nibiru_proto.proto.cosmos.auth.v1beta1 import query_pb2 as auth_query
from nibiru_proto.proto.cosmos.auth.v1beta1 import query_pb2_grpc as auth_query_grpc
from nibiru_proto.proto.cosmos.authz.v1beta1 import query_pb2 as authz_query
from nibiru_proto.proto.cosmos.authz.v1beta1 import query_pb2_grpc as authz_query_grpc
from nibiru_proto.proto.cosmos.bank.v1beta1 import query_pb2 as bank_query
from nibiru_proto.proto.cosmos.bank.v1beta1 import query_pb2_grpc as bank_query_grpc
from nibiru_proto.proto.cosmos.base.abci.v1beta1 import abci_pb2 as abci_type
from nibiru_proto.proto.cosmos.base.tendermint.v1beta1 import (
    query_pb2 as tendermint_query,
)
from nibiru_proto.proto.cosmos.base.tendermint.v1beta1 import (
    query_pb2_grpc as tendermint_query_grpc,
)
from nibiru_proto.proto.cosmos.tx.v1beta1 import service_pb2 as tx_service
from nibiru_proto.proto.cosmos.tx.v1beta1 import service_pb2_grpc as tx_service_grpc
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

        self.stubCosmosTendermint = tendermint_query_grpc.ServiceStub(
            self.chain_channel
        )
        self.stubAuth = auth_query_grpc.QueryStub(self.chain_channel)
        self.stubAuthz = authz_query_grpc.QueryStub(self.chain_channel)
        self.stubBank = bank_query_grpc.QueryStub(self.chain_channel)
        self.stubTx = tx_service_grpc.ServiceStub(self.chain_channel)

        self.timeout_height = 1

        # Query services
        self.spot = query_clients.SpotQueryClient(self.chain_channel)
        self.perp = query_clients.PerpQueryClient(self.chain_channel)
        self.vpool = query_clients.VpoolQueryClient(self.chain_channel)
        self.epoch = query_clients.EpochQueryClient(self.chain_channel)
        self.auth = query_clients.AuthQueryClient(self.chain_channel)
        self.staking = query_clients.StakingQueryClient(self.chain_channel)
        self.util = query_clients.UtilQueryClient(self.chain_channel)

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

    def get_block_by_height(
        self, height: int
    ) -> tendermint_query.GetBlockByHeightResponse:
        """
        Returns the block specified by height

        Args:
            height: the height of the block

        Returns:
            tendermint_query.GetBlockByHeightResponse: the block info

        """
        req = tendermint_query.GetBlockByHeightRequest(height=height)
        return self.stubCosmosTendermint.GetBlockByHeight(req)

    def get_blocks_by_height(
        self, start_height: int, end_height: int = None
    ) -> Generator[tendermint_query.GetBlockByHeightResponse, None, None]:
        """
        Iterate through all the blocks in the chain and yield the output of the block one by one.
        If no end_height is specified, iterate until the current latest block is reached.

        Args:
            start_height (int): The starting block height
            end_height (int, optional): The last block height to query. Defaults to None.

        Yields:
            Generator[tendermint_query.GetBlockByHeightResponse, None, None]
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
    def get_latest_block(self) -> tendermint_query.GetLatestBlockResponse:
        """
        Returns the last block

        Returns:
            tendermint_query.GetLatestBlockResponse: the last block information

        """
        req = tendermint_query.GetLatestBlockRequest()
        return self.stubCosmosTendermint.GetLatestBlock(req)

    def get_version(self) -> str:
        """
        Returns the application version

        Returns:
            str: the version of the app

        """
        req = tendermint_query.GetNodeInfoRequest()
        version = self.stubCosmosTendermint.GetNodeInfo(req).application_version.version

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

    def get_account(self, address: str) -> Optional[auth_type.BaseAccount]:
        """
        Returns the account info from address

        Args:
            address: the address of the account

        Returns:
            Optional[auth_type.BaseAccount]: the account information, none if not found

        """
        try:
            account_any = self.stubAuth.Account(
                auth_query.QueryAccountRequest(address=address)
            ).account
            account = auth_type.BaseAccount()
            if account_any.Is(account.DESCRIPTOR):
                account_any.Unpack(account)
                return account
        except:
            return None

    def get_request_id_by_tx_hash(self, tx_hash: bytes) -> List[int]:
        tx = self.stubTx.GetTx(tx_service.GetTxRequest(hash=tx_hash))
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
            req = tx_service.SimulateRequest(tx_bytes=tx_byte)
            return self.stubTx.Simulate.__call__(req), True
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
        req = tx_service.BroadcastTxRequest(
            tx_bytes=tx_byte, mode=tx_service.BroadcastMode.BROADCAST_MODE_SYNC
        )
        result = self.stubTx.BroadcastTx.__call__(req)
        return result.tx_response

    def send_tx_async_mode(self, tx_byte: bytes) -> abci_type.TxResponse:
        """
        Sends a transaction in async mode

        Args:
            tx_byte: the tx in bytes

        Returns:
            abci_type.TxResponse: the tx response

        """
        req = tx_service.BroadcastTxRequest(
            tx_bytes=tx_byte, mode=tx_service.BroadcastMode.BROADCAST_MODE_ASYNC
        )
        result = self.stubTx.BroadcastTx.__call__(req)
        return result.tx_response

    def send_tx_block_mode(self, tx_byte: bytes) -> abci_type.TxResponse:
        """
        Sends a transaction in block mode

        Args:
            tx_byte: the tx in bytes

        Returns:
            abci_type.TxResponse: the tx response

        """
        req = tx_service.BroadcastTxRequest(
            tx_bytes=tx_byte, mode=tx_service.BroadcastMode.BROADCAST_MODE_BLOCK
        )
        result = self.stubTx.BroadcastTx.__call__(req)
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
        return self.stubAuthz.Grants(
            authz_query.QueryGrantsRequest(
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
            self.stubBank.AllBalances(
                bank_query.QueryAllBalancesRequest(address=address)
            )
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
            self.stubBank.Balance(
                bank_query.QueryBalanceRequest(address=address, denom=denom)
            )
        )
