from google.protobuf.json_format import MessageToDict
from grpc import Channel
from nibiru_proto.proto.perp.v1 import query_pb2 as perp_type
from nibiru_proto.proto.perp.v1 import query_pb2_grpc as perp_query

from nibiru.query_clients.util import QueryClient, deserialize
from nibiru.utils import from_sdk_dec


class PerpQueryClient(QueryClient):
    """
    Perp allows to query the endpoints made available by the Nibiru Chain's PERP module.
    """

    def __init__(self, channel: Channel):
        self.api = perp_query.QueryStub(channel)

    def params(self):
        """
        Get the parameters of the perp module.

        Output sample::

            {
                "feePoolFeeRatio": 0.001,
                "ecosystemFundFeeRatio": 0.001,
                "liquidationFeeRatio": 0.025,
                "partialLiquidationRatio": 0.25,
                "epochIdentifier": "30 min",
                "twapLookbackWindow": "900s"
            }

        Returns:
            dict: The current parameters for the perpetual module
        """
        proto_output: perp_type.QueryParamsResponse = self.query(
            api_callable=self.api.Params,
            req=perp_type.QueryParamsRequest(),
            should_deserialize=False,
        )

        output = MessageToDict(proto_output)["params"]

        sdk_dec_fields = [
            "feePoolFeeRatio",
            "ecosystemFundFeeRatio",
            "liquidationFeeRatio",
            "partialLiquidationRatio",
        ]

        for field in sdk_dec_fields:
            output[field] = from_sdk_dec(output[field])

        return output

    def trader_position(self, token_pair: str, trader: str) -> dict:
        """
        Get the trader position. Returns information about position notional, margin ratio
        unrealized pnl, size of the position etc.

        Args:
            token_pair (str): The token pair
            trader (str): The trader address

        Sample output::

            {
                "position": {
                    "traderAddress": "nibi1zaavvzxez0elund",
                    "pair": {
                        "token0": "axlwbtc",
                        "token1": "unusd"
                    },
                    "size": 11.241446725317692,
                    "margin": 45999.99999999999,
                    "openNotional": 230000.0,
                    "lastUpdateCumulativePremiumFraction": "0",
                    "blockNumber": "278"
                },
                "positionNotional": 230000.0,
                "unrealizedPnl": 1.024e-20,
                "marginRatioMark": 0.2,
                "marginRatioIndex": 0.2
            }

        Returns:
            dict: The output of the query
        """
        req = perp_type.QueryTraderPositionRequest(
            token_pair=token_pair,
            trader=trader,
        )

        proto_output: perp_type.QueryTraderPositionResponse = self.query(
            api_callable=self.api.QueryTraderPosition, req=req, should_deserialize=False
        )

        return deserialize(proto_output)
