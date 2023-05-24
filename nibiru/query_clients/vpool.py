from grpc import Channel
from nibiru_proto.proto.vpool.v1 import query_pb2 as vpool_type
from nibiru_proto.proto.vpool.v1 import query_pb2_grpc as vpool_query
from nibiru_proto.proto.vpool.v1.state_pb2 import Direction as pbDirection

from nibiru.pytypes import Direction
from nibiru.query_clients.util import QueryClient


class VpoolQueryClient(QueryClient):
    """
    VPool allows to query the endpoints made available by the Nibiru Chain's VPOOL module.
    """

    def __init__(self, channel: Channel):
        self.api = vpool_query.QueryStub(channel)

    def reserve_assets(self, pair: str):
        """
        Returns the reserves of the vpool

        Example Return Value::

        ```json
        {
          "base_asset_reserve": "142621265.346706602199856348",
          "quote_asset_reserve": "2401396363770.998849167876702560"
        }
        ```

        Args:
            pair: the pair in "base:quote" format

        Returns:
            dict: the reserves of the vpool

        """
        req = vpool_type.QueryReserveAssetsRequest(pair=pair)
        return self.query(self.api.ReserveAssets, req)

    def all_pools(self):
        """
        Returns information about all the existing vpools

        Example Return Value::

        ```json
        {
            "pools": [
                {
                    "pair": "ubtc:unusd",
                    "base_asset_reserve": "142621265.346706602199856348",
                    "quote_asset_reserve": "2401396363770.998849167876702560",
                    "config": {
                        "trade_limit_ratio": "0.100000000000000000",
                        "fluctuation_limit_ratio": "0.100000000000000000",
                        "max_oracle_spread_ratio": "0.100000000000000000",
                        "maintenance_margin_ratio": "0.062500000000000000",
                        "max_leverage": "10.000000000000000000"
                    }
                },...
            ],
            "prices": [
                {
                    "pair": "ubtc:unusd",
                    "mark_price": "16837.575784601967733255",
                    "index_price": "16810.222187500000000000",
                    "twap_mark": "16843.132913821956433353",
                    "swap_invariant": "342490188000000000000",
                    "block_number": "432541"
                },
            ]
        }
        ```

        Returns:
            dict: the list of existing pools

        """
        req = vpool_type.QueryAllPoolsRequest()
        resp = self.query(self.api.AllPools, req)
        for _, prices in enumerate(resp["prices"]):
            prices["index_price"] = cast_str_to_float_safely(prices["index_price"])
            prices["twap_mark"] = cast_str_to_float_safely(prices["twap_mark"])
        return resp

    def base_asset_price(self, pair: str, direction: Direction, base_asset_amount: str):
        """
        Returns the price at which a base asset amount is valued in quote

        Example Return Value::

        ```json
        {
          "price_in_quote_denom": "16837.575682263963270039"
        }
        ```

        Args:
            pair: the pair in "base:quote" format
            direction(Direction): the direction of the operation (add or remove)
            base_asset_amount: the amount of base we want to know the price in quote

        Returns:
            dict: the price of the asset in quote
        """
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
    """
    Cast a string to float safely, if it fails it returns 0.

    Args:
        number_str: the number in string

    Returns:
        number(float): the number as float

    """
    try:
        number = float(number_str)
    except:
        number = float(0)
    return number
