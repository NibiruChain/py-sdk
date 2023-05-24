from typing import Dict, List, Union

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

        Example Return Value::

        ```json
        {
          "feePoolFeeRatio": 0.001,
          "ecosystemFundFeeRatio": 0.001,
          "liquidationFeeRatio": 0.025,
          "partialLiquidationRatio": 0.25,
          "epochIdentifier": "30 min",
          "twapLookbackWindow": "900s"
        }
        ```

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

    def position(self, pair: str, trader: str) -> dict:
        """
        Get the trader position. Returns information about position notional, margin ratio
        unrealized pnl, size of the position etc.

        Args:
            pair (str): The token pair
            trader (str): The trader address

        Example Return Value::

        ```json
        {
          "position": {
            "traderAddress": "nibi1zaavvzxez0elund",
            "pair": "ubtc:unusd",
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
        ```

        Returns:
            dict: The output of the query
        """
        req = perp_type.QueryPositionRequest(
            pair=pair,
            trader=trader,
        )

        proto_output: perp_type.QueryPositionResponse = self.query(
            api_callable=self.api.QueryPosition, req=req, should_deserialize=False
        )

        return deserialize(proto_output)

    def all_positions(self, trader: str) -> Dict[str, dict]:
        """
        Args:
            trader (str): Address of the owner of the positions

        Returns:
            Dict[str, dict]: All of the open positions for the 'trader'.

        Example Return Value:

        ```json
        {
          "ubtc:unusd": {
            "block_number": 1137714,
            "margin_ratio_index": 0.0,
            "margin_ratio_mark": 0.09999999999655101,
            "position": {
            "block_number": 1137714,
            "latest_cumulative_premium_fraction": 17233.436302191654,
            "margin": 10.0,
            "open_notional": 100.0,
            "pair": "ubtc:unusd",
            "size": -0.00545940925278242,
            "trader_address": "nibi10gm4kys9yyrlqpvj05vqvjwvje87gln8nsm8wa"
            },
            "position_notional": 100.0,
            "unrealized_pnl": -5.079e-15
          }
        }
        ```
        """
        req = perp_type.QueryPositionsRequest(
            trader=trader,
        )

        proto_output: perp_type.QueryPositionsResponse = self.query(
            api_callable=self.api.QueryPositions, req=req, should_deserialize=False
        )
        proto_as_dict: dict[str, list] = deserialize(proto_output)

        position_resps: Union[List[dict], None] = proto_as_dict.get("positions")
        if position_resps is None:
            return proto_as_dict

        positions_map: Dict[str, dict] = {}
        for position_resp in position_resps:
            pair = position_resp["position"]["pair"]
            positions_map[pair] = position_resp

        return positions_map
