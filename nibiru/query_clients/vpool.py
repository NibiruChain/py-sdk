from grpc import Channel
from nibiru_proto.proto.vpool.v1 import query_pb2 as vpool_type
from nibiru_proto.proto.vpool.v1 import query_pb2_grpc as vpool_query
from nibiru_proto.proto.vpool.v1.vpool_pb2 import Direction as pbDirection

from nibiru.common import Direction
from nibiru.query_clients.util import QueryClient


class VpoolQueryClient(QueryClient):
    """
    VPool allows to query the endpoints made available by the Nibiru Chain's VPOOL module.
    """

    def __init__(self, channel: Channel):
        self.api = vpool_query.QueryStub(channel)

    def reserve_assets(self, pair: str):
        req = vpool_type.QueryReserveAssetsRequest(pair=pair)
        return self.query(self.api.ReserveAssets, req)

    def all_pools(self):
        req = vpool_type.QueryAllPoolsRequest()
        resp = self.query(self.api.AllPools, req)
        for _, prices in enumerate(resp["prices"]):
            prices["index_price"] = cast_str_to_float_safely(prices["index_price"])
            prices["twap_mark"] = cast_str_to_float_safely(prices["twap_mark"])
        return resp

    def base_asset_price(self, pair: str, direction: Direction, base_asset_amount: str):
        dir_pb = pbDirection.DIRECTION_UNSPECIFIED
        if direction == Direction.ADD:
            dir_pb = pbDirection.ADD_TO_POOL
        elif direction == Direction.REMOVE:
            dir_pb = pbDirection.REMOVE_FROM_POOL

        req = vpool_type.QueryBaseAssetPriceRequest(
            pair=pair, direction=dir_pb, base_asset_amount=base_asset_amount
        )
        return self.query(self.api.BaseAssetPrice, req)


def cast_str_to_float_safely(number_str: str) -> float:
    try:
        number = float(number_str)
    except:
        number = float(0)
    return number
