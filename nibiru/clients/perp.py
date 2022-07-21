from grpc import Channel

from nibiru.proto.perp.v1 import query_pb2 as perp_type
from nibiru.proto.perp.v1 import query_pb2_grpc as perp_query

from .util import deserialize


class Perp:
    """
    Perp allows to query the endpoints made available by the Nibiru Chain's PERP module.
    """

    def __init__(self, channel: Channel):
        self.api = perp_query.QueryStub(channel)

    def params(self):
        req = perp_type.QueryParamsRequest()
        return deserialize(self.api.Params(req))

    def trader_position(self, token_pair: str, trader: str):
        req = perp_type.QueryTraderPositionRequest(
            token_pair=token_pair,
            trader=trader,
        )
        return deserialize(self.api.TraderPosition(req))
