from typing import List

from google.protobuf.json_format import MessageToDict
from grpc import Channel
from nibiru_proto.proto.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest
from nibiru_proto.proto.spot.v1 import query_pb2 as spot_type
from nibiru_proto.proto.spot.v1 import query_pb2_grpc as spot_query

from nibiru.pytypes import Coin
from nibiru.query_clients.util import QueryClient
from nibiru.utils import format_fields_nested, from_sdk_dec_n


class SpotQueryClient(QueryClient):
    """
    Spot allows to query the endpoints made available by the Nibiru Chain's SPOT module.
    """

    def __init__(self, channel: Channel):
        self.api = spot_query.QueryStub(channel)

    def params(self) -> dict:
        """
        Requests the parameters of the spot module.

        Example Return Value::

            {
                "startingPoolNumber": "1",
                "poolCreationFee": [
                    {
                        "denom": "unibi",
                        "amount": 1000.0
                    }
                ],
                "whitelistedAsset": [
                    "unibi",
                    "uusdc",
                    "unusd",
                    "stake"
                ]
            }

        Returns:
            dict: The parameters fo the spot module.
        """
        proto_output = self.query(
            api_callable=self.api.Params,
            req=spot_type.QueryParamsRequest(),
            should_deserialize=False,
        )

        output: dict = MessageToDict(proto_output)["params"]

        output["poolCreationFee"] = [
            {"denom": item["denom"], "amount": from_sdk_dec_n(item["amount"])}
            for item in output["poolCreationFee"]
        ]
        return output

    def pools(self, **kwargs):
        """
        Return all available pools in the spot module.

        Example Return Value::

            [
                {
                    "id": "1",
                    "address": "nibi1w00c7pqkr5z7ptewg5z87j2ncvxd88w43ug679",
                    "poolParams": {
                        "swapFee": 0.02,
                        "exitFee": 0.1
                    },
                    "poolAssets": [
                        {
                            "token": {
                                "denom": "unibi",
                                "amount": 0.001
                            },
                            "weight": "53687091200000000"
                        },
                        {
                            "token": {
                                "denom": "unusd",
                                "amount": 0.01
                            },
                            "weight": "53687091200000000"
                        }
                    ],
                    "totalWeight": "107374182400000000",
                    "totalShares": {
                        "denom": "nibiru/pool/1",
                        "amount": 100000000000000.0
                    }
                }
            ]


        Args:
            key (bytes): The page key for the next page. Only key or offset should be set
            offset (int): The number of entries to skip. Only offset or key should be set
            limit (int): The number of max results in the page
            count_total (bool): Indicates if the response should contain the total number of results
            reverse (bool): Indicates if the results should be returned in descending order

        Returns:
            dict: The output of the query
        """
        proto_output = self.query(
            api_callable=self.api.Pools,
            req=spot_type.QueryPoolsRequest(
                pagination=PageRequest(
                    key=kwargs.get("key"),
                    offset=kwargs.get("offset"),
                    limit=kwargs.get("limit"),
                    count_total=kwargs.get("count_total"),
                    reverse=kwargs.get("reverse"),
                ),
            ),
            should_deserialize=False,
        )

        output: dict = MessageToDict(proto_output).get("pools")
        if output is None:
            output = {}

        return format_fields_nested(
            object=format_fields_nested(
                object=output,
                fn=lambda x: from_sdk_dec_n(x, 18),
                fields=["swapFee", "exitFee"],
            ),
            fn=lambda x: from_sdk_dec_n(x, 6),
            fields=["amount"],
        )

    def total_liquidity(self) -> dict:
        """
        Returns the total amount of liquidity for the spot module

        Example Return Value::

            {
                "liquidity": [
                    {
                        "denom": "unibi",
                        "amount": 0.001
                    },
                    {
                        "denom": "unusd",
                        "amount": 0.01
                    }
                ]
            }

        Returns:
            dict: The total liquidity of the protocol
        """
        proto_output = self.query(
            api_callable=self.api.TotalLiquidity,
            req=spot_type.QueryTotalLiquidityRequest(),
            should_deserialize=False,
        )

        output = MessageToDict(proto_output)
        return format_fields_nested(
            object=output, fn=lambda x: from_sdk_dec_n(x, 6), fields=["amount"]
        )

    def total_pool_liquidity(self, pool_id: int) -> dict:
        """
        Returns the total liquidity for a specific pool id

        Example Return Value::

            {
                "liquidity": [
                    {
                        "denom": "unibi",
                        "amount": 0.001
                    },
                    {
                        "denom": "unusd",
                        "amount": 0.01
                    }
                ]
            }

        Args:
            pool_id (int): the id of the pool

        Returns:
            dict: The total liquidity for the pool
        """
        proto_output = self.query(
            api_callable=self.api.TotalPoolLiquidity,
            req=spot_type.QueryTotalPoolLiquidityRequest(pool_id=pool_id),
            should_deserialize=False,
        )

        output = MessageToDict(proto_output)
        return format_fields_nested(
            object=output, fn=lambda x: from_sdk_dec_n(x, 6), fields=["amount"]
        )

    def total_shares(self, pool_id: int) -> dict:
        """
        Returns the total amount of shares for the pool specified

        Example Return Value::

            {
                "totalShares": {
                    "denom": "nibiru/pool/1",
                    "amount": 100000000000000.0
                }
            }

        Args:
            pool_id (int): The id of the pool

        Returns:
            dict: The amount of shares for the pool
        """
        proto_output = self.query(
            api_callable=self.api.TotalShares,
            req=spot_type.QueryTotalSharesRequest(pool_id=pool_id),
            should_deserialize=False,
        )

        output = MessageToDict(proto_output)
        return format_fields_nested(
            object=output, fn=lambda x: from_sdk_dec_n(x, 6), fields=["amount"]
        )

    def spot_price(
        self, pool_id: int, token_in_denom: str, token_out_denom: str
    ) -> dict:
        """
        Returns the spot price of the pool using token in as base and token out as quote

        Args:
            pool_id (int): _description_
            token_in_denom (str): _description_
            token_out_denom (str): _description_

        Returns:
            dict: _description_
        """
        proto_output = self.query(
            api_callable=self.api.SpotPrice,
            req=spot_type.QuerySpotPriceRequest(
                pool_id=pool_id,
                token_in_denom=token_in_denom,
                token_out_denom=token_out_denom,
            ),
            should_deserialize=False,
        )

        output = MessageToDict(proto_output)
        return format_fields_nested(object=output, fn=float, fields=["spotPrice"])

    def estimate_swap_exact_amount_in(
        self, pool_id: int, token_in: Coin, token_out_denom: str
    ) -> dict:
        """
        Estimate the output of the swap with the current reserves

        Example Return Value::

            {
                "tokenOut": {
                    "denom": "unusd",
                    "amount": 0.004948999999999999
                }
            }

        Args:
            pool_id (int): The pool id to query
            token_in (Coin): The amount of tokens to provide
            token_out_denom (str): The denomination of the token out

        Returns:
            dict: The output of the query
        """
        proto_output = self.query(
            api_callable=self.api.EstimateSwapExactAmountIn,
            req=spot_type.QuerySwapExactAmountInRequest(
                pool_id=pool_id,
                token_in=token_in._generate_proto_object(),
                token_out_denom=token_out_denom,
            ),
            should_deserialize=False,
        )

        output = MessageToDict(proto_output)
        return format_fields_nested(
            object=output, fn=lambda x: from_sdk_dec_n(x, 6), fields=["amount"]
        )

    def estimate_join_exact_amount_in(
        self, pool_id: int, tokens_ins: List[Coin]
    ) -> dict:
        """
        Estimate the number of share given for a join pool operation

        Example Return Value::

            {
                "poolSharesOut": 100000000000000.0,
                "remCoins": [
                    {
                        "denom": "unibi",
                        "amount": 0.999
                    }
                ]
            }

        Args:
            pool_id (int): The id of the pool to query
            tokens_ins (List[Coin]): The amount of tokens provided

        Returns:
            dict: The output of the query
        """
        proto_output = self.query(
            api_callable=self.api.EstimateJoinExactAmountIn,
            req=spot_type.QueryJoinExactAmountInRequest(
                pool_id=pool_id,
                tokens_in=[
                    tokens_in._generate_proto_object() for tokens_in in tokens_ins
                ],
            ),
            should_deserialize=False,
        )

        output = MessageToDict(proto_output)
        return format_fields_nested(
            object=output,
            fn=lambda x: from_sdk_dec_n(x, 6),
            fields=["amount", "poolSharesOut"],
        )

    def estimate_exit_exact_amount_in(self, pool_id: int, num_shares: int) -> dict:
        """
        Estimate the output of an exit pool transaction with the current level of reserves

        Example Return Value::

            {
                "tokensOut": [
                    {
                        "denom": "unibi",
                        "amount": 1000.5
                    },
                    {
                        "denom": "unusd",
                        "amount": 100.2
                    }
                ]
            }

        Args:
            pool_id (int): The id of the pool to query
            num_shares (int): The number of shares to provide

        Returns:
            dict: The output of the query
        """
        proto_output = self.query(
            api_callable=self.api.EstimateExitExactAmountIn,
            req=spot_type.QueryExitExactAmountInRequest(
                pool_id=pool_id, pool_shares_in=str(num_shares * 1e6)
            ),
            should_deserialize=False,
        )
        output = MessageToDict(proto_output)
        return format_fields_nested(
            object=output, fn=lambda x: from_sdk_dec_n(x, 6), fields=["amount"]
        )
