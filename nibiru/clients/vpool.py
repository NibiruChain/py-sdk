from grpc import Channel

from nibiru.common import Direction
from nibiru.proto.vpool.v1 import query_pb2 as vpool_type
from nibiru.proto.vpool.v1 import query_pb2_grpc as vpool_query
from nibiru.proto.vpool.v1.vpool_pb2 import Direction as pbDirection


class VPool:
    """
    VPool allows to query the endpoints made available by the Nibiru Chain's VPOOL module.
    """

    def __init__(self, channel: Channel):
        self.api = vpool_query.QueryStub(channel)

    def reserve_assets(self, pair: str):
        req = vpool_type.QueryReserveAssetsRequest(pair=pair)
        return self.api.ReserveAssets(req)

    def all_pools(self):
        req = vpool_type.QueryAllPoolsRequest()
        return self.api.AllPools(req)

    def base_asset_price(self, pair: str, direction: Direction, base_asset_amount: str):
        dir = pbDirection.DIRECTION_UNSPECIFIED
        if direction == Direction.ADD:
            dir = pbDirection.ADD_TO_POOL
        elif direction == Direction.REMOVE:
            dir = pbDirection.REMOVE_FROM_POOL

        req = vpool_type.QueryBaseAssetPriceRequest(pair=pair, direction=dir, base_asset_amount=base_asset_amount)
        return self.api.BaseAssetPrice(req)
