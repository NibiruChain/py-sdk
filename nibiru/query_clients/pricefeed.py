from grpc import Channel
from nibiru_proto.proto.pricefeed import query_pb2 as pf_type
from nibiru_proto.proto.pricefeed import query_pb2_grpc as pf_query

from nibiru.query_clients.util import QueryClient


class PricefeedQueryClient(QueryClient):
    """
    Pricefeed allows to query the endpoints made available by the Nibiru Chain's Pricefeed module.
    """

    def __init__(self, channel: Channel):
        self.api = pf_query.QueryStub(channel)

    def params(self):
        req = pf_type.QueryParamsRequest()
        return self.query(self.api.QueryParams, req)

    def price(self, pair_id: str):
        req = pf_type.QueryPriceRequest(
            pair_id=pair_id,
        )
        return self.query(self.api.QueryPrice, req)

    def prices(self):
        req = pf_type.QueryPricesRequest()
        return self.query(self.api.QueryPrices, req)

    def raw_prices(self, pair_id: str):
        req = pf_type.QueryRawPricesRequest(
            pair_id=pair_id,
        )
        return self.query(self.api.QueryRawPrices, req)

    def oracles(self, pair_id: str):
        req = pf_type.QueryOraclesRequest(
            pair_id=pair_id,
        )
        return self.query(self.api.QueryOracles, req)

    def markets(self):
        req = pf_type.QueryMarketsRequest()
        return self.query(self.api.QueryMarkets, req)
