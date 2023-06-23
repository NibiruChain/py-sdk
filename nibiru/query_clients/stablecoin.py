from google.protobuf.json_format import MessageToDict
from grpc import Channel
from nibiru_proto.proto.stablecoin import query_pb2 as stablecoin_type
from nibiru_proto.proto.stablecoin import query_pb2_grpc as stablecoin_query

from nibiru.query_clients.util import QueryClient
from nibiru.utils import format_fields_nested, from_sdk_dec_n


class StablecoinQueryClient(QueryClient):
    """
    Stablecoin allows to query the endpoints made available by the Nibiru Chain's
    Stablecoin module.
    """

    def __init__(self, channel: Channel):
        self.api = stablecoin_query.QueryStub(channel)

    def params(self) -> dict:
        """
        Requests the parameters of the stablecoin module.

        Example Return Value:
        {
            "params": {
                "coll_ratio": "140000",
                "fee_ratio": "2000",
                "ef_fee_ratio": "500000",
                "bonus_rate_recoll": "2000",
                "distr_epoch_identifier": "15 min",
                "adjustment_step": "2500",
                "price_lower_bound": "999900",
                "price_upper_bound": "1000100",
                "is_collateral_ratio_valid": true
            }
        }

        Returns:
            dict: The parameters fo the stablecoin module.
        """
        return self.query(
            api_callable=self.api.Params,
            req=stablecoin_type.QueryParamsRequest(),
            should_deserialize=True,
        )

    def circulating_supplies(self, **kwargs):
        """
        Return circulating supplies value of the stablecoin.

        Example Return Value::
        {
          "nibi": {
            "denom": "unibi",
            "amount": "4067118588898816"
          },
          "nusd": {
            "denom": "unusd",
            "amount": "2009322333444555"
          }
        }
        Returns:
            dict: The output of the query
        """
        proto_output = self.query(
            api_callable=self.api.CirculatingSupplies,
            req=stablecoin_type.QueryCirculatingSupplies(),
            should_deserialize=False,
        )
        output = MessageToDict(proto_output)
        return format_fields_nested(
            object=output, fn=lambda x: from_sdk_dec_n(x, 6), fields=["amount"]
        )

    def liquidity_ratio_info(self) -> dict:
        """
        Returns liquidity ratio from the stablecoin module

        Example Return Value:
        {
          "info": {
            "liquidity_ratio": "0.005214231356709351",
            "upper_band": "0.005219445588066060",
            "lower_band": "0.005209017125352642"
          }
        }

        Returns:
            dict: liquidity ratio info.
        """
        return self.query(
            api_callable=self.api.LiquidityRatioInfo,
            req=stablecoin_type.QueryLiquidityRatioInfoRequest(),
        )
