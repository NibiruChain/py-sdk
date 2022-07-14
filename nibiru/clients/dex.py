from typing import List

from grpc import Channel

from nibiru.proto.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest
from nibiru.proto.cosmos.base.v1beta1 import coin_pb2 as cosmos_base_coin_pb
from nibiru.proto.dex.v1 import query_pb2 as dex_type
from nibiru.proto.dex.v1 import query_pb2_grpc as dex_query


class Dex:
    """
    Dex allows to query the endpoints made available by the Nibiru Chain's DEX module.
    """

    def __init__(self, channel: Channel):
        self.api = dex_query.QueryStub(channel)

    def params(self):
        req = dex_type.QueryParamsRequest()
        return self.api.Params(req)

    def pool_number(self):
        req = dex_type.QueryPoolsRequest()
        return self.api.PoolNumber(req)

    def pool(self, pool_id: int):
        req = dex_type.QueryPoolRequest(poolId=pool_id)
        return self.api.Pool(req)

    def pools(self, **kwargs):
        '''
        Returns all available pools
        Parameters:
            key (bytes): The page key for the next page. Only key or offset should be set
            offset (int): The number of entries to skip. Only offset or key should be set
            limit (int): The number of max results in the page
            count_total (bool): Indicates if the response should contain the total number of results
            reverse (bool): Indicates if the results should be returned in descending order
        '''
        req = dex_type.QueryPoolsRequest(
            pagination=PageRequest(
                key=kwargs.get("key"),
                offset=kwargs.get("offset"),
                limit=kwargs.get("limit"),
                count_total=kwargs.get("count_total"),
                reverse=kwargs.get("reverse"),
            ),
        )
        return self.api.Pools(req)

    def pool_params(self, pool_id: int):
        req = dex_type.QueryPoolParamsRequest(poolId=pool_id)
        return self.api.PoolParams(req)

    def num_pools(self):
        req = dex_type.QueryNumPoolsRequest()
        return self.api.NumPools(req)

    def total_liquidity(self):
        req = dex_type.QueryTotalLiquidityRequest()
        return self.api.TotalLiquidity(req)

    def total_pool_liquidity(self, pool_id: int):
        req = dex_type.QueryTotalPoolLiquidityRequest(poolId=pool_id)
        return self.api.TotalPoolLiquidity(req)

    def total_shares(self, pool_id: int):
        req = dex_type.QueryTotalSharesRequest(poolId=pool_id)
        return self.api.TotalShares(req)

    def spot_price(self, pool_id: int, token_in_denom: str, token_out_denom: str):
        req = dex_type.QuerySpotPriceRequest(
            poolId=pool_id,
            tokenInDenom=token_in_denom,
            tokenOutDenom=token_out_denom,
        )
        return self.api.SpotPrice(req)

    def estimate_swap_exact_amount_in(self, pool_id: int, token_in: cosmos_base_coin_pb.Coin, token_out_denom: str):
        req = dex_type.QuerySwapExactAmountInRequest(
            poolId=pool_id,
            tokenIn=token_in,
            tokenOutDenom=token_out_denom,
        )
        return self.api.EstimateSwapExactAmountIn(req)

    def estimate_swap_exact_amount_out(self, pool_id: int, token_out: cosmos_base_coin_pb.Coin, token_in_denom: str):
        req = dex_type.QuerySwapExactAmountOutRequest(
            poolId=pool_id,
            tokenOut=token_out,
            tokenInDenom=token_in_denom,
        )
        return self.api.EstimateSwapExactAmountOut(req)

    def estimate_join_exact_amount_in(self, pool_id: int, tokens_in: List[cosmos_base_coin_pb.Coin]):
        req = dex_type.QueryJoinExactAmountInRequest(
            poolId=pool_id,
            tokensIn=tokens_in,
        )
        return self.api.EstimateJoinExactAmountIn(req)

    def estimate_join_exact_amount_out(self, pool_id: int):
        req = dex_type.QueryJoinExactAmountOutRequest(
            poolId=pool_id,
        )
        return self.api.EstimateJoinExactAmountOut(req)

    def estimate_exit_exact_amount_in(self, pool_id: int, num_shares: int):
        req = dex_type.QueryExitExactAmountInRequest(poolId=pool_id, poolSharesIn=num_shares)
        return self.api.EstimateExitExactAmountIn(req)

    def estimate_exit_exact_amount_out(self, pool_id: int):
        req = dex_type.QueryExitExactAmountOutRequest(
            poolId=pool_id,
        )
        return self.api.EstimateExitExactAmountOut(req)
