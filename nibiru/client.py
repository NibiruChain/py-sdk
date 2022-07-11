import os
import time
import grpc
import aiocron
import datetime
from http.cookies import SimpleCookie
from typing import List, Optional, Tuple, Union

from .clients import (
    Dex as DexClient, Perp as PerpClient,
)

from .exceptions import NotFoundError

from .proto.cosmos.base.abci.v1beta1 import abci_pb2 as abci_type

from .proto.cosmos.base.tendermint.v1beta1 import (
    query_pb2_grpc as tendermint_query_grpc,
    query_pb2 as tendermint_query,
)

from .proto.cosmos.auth.v1beta1 import (
    query_pb2_grpc as auth_query_grpc,
    query_pb2 as auth_query,
    auth_pb2 as auth_type,
)
from .proto.cosmos.authz.v1beta1 import (
    query_pb2_grpc as authz_query_grpc,
    query_pb2 as authz_query,
    authz_pb2 as authz_type,
)
from .proto.cosmos.bank.v1beta1 import (
    query_pb2_grpc as bank_query_grpc,
    query_pb2 as bank_query,
)
from .proto.cosmos.tx.v1beta1 import (
    service_pb2_grpc as tx_service_grpc,
    service_pb2 as tx_service,
)
from .proto.dex.v1 import (
    query_pb2_grpc as dex_query,
    query_pb2 as dex_type,
)
from .proto.pricefeed import (
    query_pb2_grpc as pricefeed_query,
    query_pb2 as pricefeed_type,
)
from .proto.lockup.v1 import (
    query_pb2_grpc as lockup_query,
    query_pb2 as lockup_type,
)
from .proto.incentivization.v1 import (
    incentivization_pb2_grpc as incentivization_query,
    incentivization_pb2 as incentivization_type,
)
from .proto.vpool.v1 import (
    query_pb2_grpc as vpool_query,
    query_pb2 as vpool_type,
)
from .proto.stablecoin import (
    query_pb2_grpc as stablecoin_query,
    query_pb2 as stablecoin_type,
)
from .proto.epochs import (
    query_pb2_grpc as epochs_query,
    query_pb2 as epochs_type,
)

from .network import Network

DEFAULT_TIMEOUTHEIGHT_SYNC_INTERVAL = 10 # seconds
DEFAULT_TIMEOUTHEIGHT = 20 # blocks
DEFAULT_SESSION_RENEWAL_OFFSET = 120 # seconds
DEFAULT_BLOCK_TIME = 3 # seconds
DEFAULT_CHAIN_COOKIE_NAME = '.chain_cookie'

# use append mode to create file if not exist
cookie_file = open(DEFAULT_CHAIN_COOKIE_NAME, "a+")
cookie_file.close()

class Client:
    def __init__(
        self,
        network: Network,
        insecure: bool = False,
        credentials: grpc.ChannelCredentials = None,
    ):

        # load root CA cert
        # if not insecure:
        #     if network.env == 'testnet':
        #         if credentials is None:
        #             with open(os.path.join(os.path.dirname(__file__), 'cert/testnet.crt'), 'rb') as f:
        #                 credentials = grpc.ssl_channel_credentials(f.read())
        #     if network.env == 'mainnet':
        #         if credentials is None:
        #             with open(os.path.join(os.path.dirname(__file__), 'cert/mainnet.crt'), 'rb') as f:
        #                 credentials = grpc.ssl_channel_credentials(f.read())

        # chain stubs
        self.chain_channel = (
            grpc.aio.insecure_channel(network.grpc_endpoint)
            if insecure else grpc.aio.secure_channel(network.grpc_endpoint, credentials)
        )
        self.insecure = insecure
        self.stubCosmosTendermint = tendermint_query_grpc.ServiceStub(self.chain_channel)
        self.stubAuth = auth_query_grpc.QueryStub(self.chain_channel)
        self.stubAuthz = authz_query_grpc.QueryStub(self.chain_channel)
        self.stubBank = bank_query_grpc.QueryStub(self.chain_channel)
        self.stubTx = tx_service_grpc.ServiceStub(self.chain_channel)

        # attempt to load from disk
        cookie_file = open(DEFAULT_CHAIN_COOKIE_NAME, "r+")
        self.chain_cookie = cookie_file.read()
        cookie_file.close()
        print("chain session cookie loaded from disk:", self.chain_cookie)

        self.exchange_cookie = ""
        self.timeout_height = 1

        # exchange stubs
        self.exchange_channel = (
            grpc.aio.insecure_channel(network.grpc_exchange_endpoint)
            if insecure else grpc.aio.secure_channel(network.grpc_exchange_endpoint, credentials)
        )
        # Query services
        self.dex = DexClient(self.exchange_channel)
        self.stubPricefeed = pricefeed_query.QueryStub(self.exchange_channel)
        self.perp = PerpClient(self.exchange_channel)
        self.stubLockup = lockup_query.QueryStub(self.exchange_channel)
        self.stubIncentivization = incentivization_query.QueryStub(self.exchange_channel)
        self.stubVpool = vpool_query.QueryStub(self.exchange_channel)
        self.stubStablecoin = stablecoin_query.QueryStub(self.exchange_channel)
        self.stubEpochs = epochs_query.QueryStub(self.exchange_channel)

        # timeout height update routine
        aiocron.crontab(
            '* * * * * */{}'.format(DEFAULT_TIMEOUTHEIGHT_SYNC_INTERVAL),
            func=self.sync_timeout_height,
            args=(),
            start=True
        )

    async def close_exchange_channel(self):
        await self.exchange_channel.close()

    async def close_chain_channel(self):
        await self.chain_channel.close()

    async def sync_timeout_height(self):
        block = await self.get_latest_block()
        self.timeout_height = block.block.header.height + DEFAULT_TIMEOUTHEIGHT

    # cookie helper methods
    async def fetch_cookie(self, chain_type):
        metadata = None
        if chain_type == "chain":
            req = tendermint_query.GetLatestBlockRequest()
            metadata = await self.stubCosmosTendermint.GetLatestBlock(req).initial_metadata()
            time.sleep(DEFAULT_BLOCK_TIME)
        # if chain_type == "exchange":
            # not sure what to do here, do we have a counterpart or can any req/resp be used??
            # req = exchange_meta_rpc_pb.VersionRequest()
            # metadata = await self.stubMeta.Version(req).initial_metadata()
        return metadata

    async def renew_cookie(self, existing_cookie, chain_type):
        metadata = None
        # format cookie date into RFC1123 standard
        cookie = SimpleCookie()
        cookie.load(existing_cookie)
        expires_at = cookie.get("grpc-cookie").get("expires")
        expires_at = expires_at.replace("-"," ")
        yyyy = "20{}".format(expires_at[12:14])
        expires_at = expires_at[:12] + yyyy + expires_at[14:]

        # parse expire field to unix timestamp
        expire_timestamp = datetime.datetime.strptime(expires_at, "%a, %d %b %Y %H:%M:%S GMT").timestamp()

        # renew session if timestamp diff < offset
        timestamp_diff = expire_timestamp - int(time.time())
        if timestamp_diff < DEFAULT_SESSION_RENEWAL_OFFSET:
            metadata = await self.fetch_cookie(chain_type)
        else:
            metadata = (("cookie", existing_cookie),)
        return metadata

    async def load_cookie(self, chain_type):
        metadata = None
        if self.insecure:
            return metadata

        if chain_type == "chain":
            if self.chain_cookie != "":
                 metadata = await self.renew_cookie(self.chain_cookie, chain_type)
                 self.set_cookie(metadata, chain_type)
            else:
                metadata = await self.fetch_cookie(chain_type)
                self.set_cookie(metadata, chain_type)

        if chain_type == "exchange":
            if self.exchange_cookie != "":
                 metadata = await self.renew_cookie(self.exchange_cookie, chain_type)
                 self.set_cookie(metadata, chain_type)
            else:
                metadata = await self.fetch_cookie(chain_type)
                self.set_cookie(metadata, chain_type)

        return metadata

    def set_cookie(self, metadata, chain_type):
        new_cookie = None
        if self.insecure:
            return new_cookie

        for k, v in metadata:
            if k == "set-cookie":
                new_cookie = v

        if new_cookie == None:
            return

        if chain_type == "chain":
            # write to client instance
            self.chain_cookie = new_cookie
            # write to disk
            cookie_file = open(DEFAULT_CHAIN_COOKIE_NAME, "w")
            cookie_file.write(new_cookie)
            cookie_file.close()
            print("chain session cookie saved to disk")

        if chain_type == "exchange":
            self.exchange_cookie = new_cookie

    # default client methods
    async def get_latest_block(self) -> tendermint_query.GetLatestBlockResponse:
        req = tendermint_query.GetLatestBlockRequest()
        return await self.stubCosmosTendermint.GetLatestBlock(req)

    async def get_account(self, address: str) -> Optional[auth_type.BaseAccount]:
        try:
            account_any = await self.stubAuth.Account(
                auth_query.QueryAccountRequest(address=address)
            ).account
            account = auth_type.BaseAccount()
            if account_any.Is(account.DESCRIPTOR):
                account_any.Unpack(account)
                return account
        except:
            return None

    async def get_request_id_by_tx_hash(self, tx_hash: bytes) -> List[int]:
        tx = await self.stubTx.GetTx(tx_service.GetTxRequest(hash=tx_hash))
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
            raise NotFoundError("Request Id is not found")
        return request_ids

    async def simulate_tx(
        self, tx_byte: bytes
    ) -> Tuple[Union[abci_type.SimulationResponse, grpc.RpcError], bool]:
        try:
            req = tx_service.SimulateRequest(tx_bytes=tx_byte)
            metadata = await self.load_cookie(chain_type="chain")
            return await self.stubTx.Simulate.__call__(req, metadata=metadata), True
        except grpc.RpcError as err:
            return err, False

    async def send_tx_sync_mode(self, tx_byte: bytes) -> abci_type.TxResponse:
        req = tx_service.BroadcastTxRequest(tx_bytes=tx_byte, mode=tx_service.BroadcastMode.BROADCAST_MODE_SYNC)
        metadata = await self.load_cookie(chain_type="chain")
        result = await self.stubTx.BroadcastTx.__call__(req, metadata=metadata)
        return result.tx_response

    async def send_tx_async_mode(self, tx_byte: bytes) -> abci_type.TxResponse:
        req = tx_service.BroadcastTxRequest(tx_bytes=tx_byte, mode=tx_service.BroadcastMode.BROADCAST_MODE_ASYNC)
        metadata = await self.load_cookie(chain_type="chain")
        result = await self.stubTx.BroadcastTx.__call__(req, metadata=metadata)
        return result.tx_response

    async def send_tx_block_mode(self, tx_byte: bytes) -> abci_type.TxResponse:
        req = tx_service.BroadcastTxRequest(tx_bytes=tx_byte, mode=tx_service.BroadcastMode.BROADCAST_MODE_BLOCK)
        metadata = await self.load_cookie(chain_type="chain")
        result = await self.stubTx.BroadcastTx.__call__(req, metadata=metadata)
        return result.tx_response

    async def get_chain_id(self) -> str:
        latest_block = await self.get_latest_block()
        return latest_block.block.header.chain_id

    async def get_grants(self, granter: str, grantee: str, **kwargs):
        return await self.stubAuthz.Grants(
            authz_query.QueryGrantsRequest(
                granter=granter,
                grantee=grantee,
                msg_type_url=kwargs.get("msg_type_url"),
            )
        )

    async def get_bank_balances(self, address: str):
        return await self.stubBank.AllBalances(
            bank_query.QueryAllBalancesRequest(
                address=address
            )
        )

    async def get_bank_balance(self, address: str, denom: str):
        return await self.stubBank.Balance(
            bank_query.QueryBalanceRequest(
                address=address,
                denom=denom
            )
        )
