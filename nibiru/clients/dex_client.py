from grpc import Channel
from nibiru.proto.cosmos.base.v1beta1 import coin_pb2 as cosmos_base_coin_pb
from nibiru.proto.dex.v1 import (
    query_pb2_grpc as dex_query,
    query_pb2 as dex_type,
)
from nibiru.proto.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest
from typing import List

class DexClient:
    def __init__(
        self,
        channel: Channel
    ):
        self.api = dex_query.QueryStub(channel)

    async def params(self):
        req = dex_type.QueryParamsRequest()
        return await self.api.Params(req)

    async def pool_number(self):
        req = dex_type.QueryPoolsRequest()
        return await self.api.PoolNumber(req)

    async def pool(self, pool_id: int):
        req = dex_type.QueryPoolRequest(poolId = pool_id)
        return await self.api.Pool(req)

    async def pools(self, **kwargs):
        req = dex_type.QueryPoolsRequest(pagination = PageRequest(
                key = kwargs.get("key"),
                offset = kwargs.get("offset"),
                limit = kwargs.get("limit"),
                countTotal = kwargs.get("count_total"),
                reverse = kwargs.get("reverse"),
            ),
        )
        return await self.api.Pools(req)

    async def pool_params(self, pool_id: int):
        req = dex_type.QueryPoolParamsRequest(poolId = pool_id)
        return await self.api.PoolParams(req)

    async def num_pools(self):
        req = dex_type.QueryNumPoolsRequest()
        return await self.api.NumPools(req)

    async def total_liquidity(self):
        req = dex_type.QueryTotalLiquidityRequest()
        return await self.api.TotalLiquidity(req)

    async def total_pool_liquidity(self, pool_id: int):
        req = dex_type.QueryTotalLiquidityRequest(poolId = pool_id)
        return await self.api.TotalPoolLiquidity(req)

    async def total_shares(self, pool_id: int):
        req = dex_type.QueryTotalSharesRequest(poolId = pool_id)
        return await self.api.TotalShares(req)

    async def spot_price(self, pool_id: int, token_in_denom: str, token_out_denom: str):
        req = dex_type.QuerySpotPriceRequest(
            poolId = pool_id,
            tokenInDenom = token_in_denom,
            tokenOutDenom = token_out_denom,
        )
        return await self.api.SpotPrice(req)

    async def estimate_swap_exact_amount_in(self, pool_id: int, token_in: cosmos_base_coin_pb.Coin, token_out_denom: str):
        req = dex_type.QuerySwapExactAmountInRequest(
            poolId = pool_id,
            tokenIn = token_in,
            tokenOutDenom = token_out_denom,
        )
        return await self.api.EstimateSwapExactAmountIn(req)

    async def estimate_swap_exact_amount_out(self, pool_id: int, token_out: cosmos_base_coin_pb.Coin, token_in_denom: str):
        req = dex_type.QuerySwapExactAmountOutRequest(
            poolId = pool_id,
            tokenOut = token_out,
            tokenInDenom = token_in_denom,
        )
        return await self.api.EstimateSwapExactAmountOut(req)

    async def estimate_join_exact_amount_in(self, pool_id: int, tokens_in: List[cosmos_base_coin_pb.Coin]):
        req = dex_type.QueryJoinExactAmountInRequest(
            poolId = pool_id,
            tokensIn = tokens_in,
        )
        return await self.api.EstimateJoinExactAmountIn(req)

    async def estimate_join_exact_amount_out(self, pool_id: int):
        req = dex_type.QueryJoinExactAmountOutRequest(
            poolId = pool_id,
        )
        return await self.api.EstimateJoinExactAmountOut(req)

    async def estimate_exit_exact_amount_in(self, pool_id: int, num_shares: int):
        req = dex_type.QueryExitExactAmountInRequest(
            poolId = pool_id,
            poolSharesIn = num_shares
        )
        return await self.api.EstimateExitExactAmountIn(req)

    async def estimate_exit_exact_amount_out(self, pool_id: int):
        req = dex_type.QueryExitExactAmountOutRequest(
            poolId = pool_id,
        )
        return await self.api.EstimateExitExactAmountOut(req)
