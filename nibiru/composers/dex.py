from typing import List

from nibiru.proto.dex.v1 import (
    tx_pb2 as dex_tx_pb,
    pool_pb2 as pool_tx_pb,
)
from nibiru.common import PoolAsset

from nibiru.proto.cosmos.base.v1beta1 import coin_pb2 as coin_pb


class Dex:
    @staticmethod
    def create_pool(creator: str, swap_fee: str, exit_fee: str, assets: List[PoolAsset]):
        pool_assets = [pool_tx_pb.PoolAsset(token=a.token, weight=a.weight) for a in assets]

        return dex_tx_pb.MsgCreatePool(
            creator = creator,
            poolParams = pool_tx_pb.PoolParams(swapFee=swap_fee, exitFee=exit_fee),
            poolAssets = pool_assets,
        )

    @staticmethod
    def join_pool(sender: str, pool_id: int, tokens: List[coin_pb.Coin]):
        return dex_tx_pb.MsgJoinPool(
            sender = sender,
            poolId = pool_id,
            tokensIn = tokens,
        )

    @staticmethod
    def exit_pool(sender: str, pool_id: int, pool_shares: coin_pb.Coin):
        return dex_tx_pb.MsgExitPool(
            sender = sender,
            poolId = pool_id,
            poolShares = pool_shares,
        )

    @staticmethod
    def swap_assets(sender: str, pool_id: int, token_in: coin_pb.Coin, token_out_denom):
        return dex_tx_pb.MsgSwapAssets(
            sender = sender,
            poolId = pool_id,
            tokenIn = token_in,
            tokenOutDenom = token_out_denom,
        )
