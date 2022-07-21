from typing import List

from nibiru.common import PoolAsset
from nibiru.composers.dex import Dex as DexComposer
from nibiru.proto.cosmos.base.v1beta1 import coin_pb2 as coin_pb

from .common import Tx


class Dex(Tx):
    def create_pool(self, creator: str, swap_fee: float, exit_fee: float, assets: List[PoolAsset], **kwargs):
        msg = DexComposer.create_pool(creator=creator, swap_fee=swap_fee, exit_fee=exit_fee, assets=assets)
        return super().execute_msg(msg, **kwargs)

    def join_pool(self, sender: str, pool_id: int, tokens: List[coin_pb.Coin], **kwargs):
        msg = DexComposer.join_pool(sender=sender, pool_id=pool_id, tokens=tokens)
        return super().execute_msg(msg, **kwargs)

    def exit_pool(self, sender: str, pool_id: int, pool_shares: coin_pb.Coin, **kwargs):
        msg = DexComposer.exit_pool(sender=sender, pool_id=pool_id, pool_shares=pool_shares)
        return super().execute_msg(msg, **kwargs)

    def swap_assets(self, sender: str, pool_id: int, token_in: coin_pb.Coin, token_out_denom, **kwargs):
        msg = DexComposer.swap_assets(
            sender=sender,
            pool_id=pool_id,
            token_in=token_in,
            token_out_denom=token_out_denom,
        )
        return super().execute_msg(msg, **kwargs)
