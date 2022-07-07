from nibiru.composers.dex_composer import DexComposer
from nibiru.common import PoolAsset

from nibiru.proto.cosmos.base.v1beta1 import coin_pb2 as coin_pb

from typing import List

from .common import Tx

class Dex(Tx):
    def create_pool(self, creator: str, swap_fee: str, exit_fee: str, assets: List[PoolAsset]):
        msg = DexComposer.create_pool(creator, swap_fee, exit_fee, assets)
        return super().execute(msg)

    def join_pool(self, sender: str, pool_id: int, tokens: List[coin_pb.Coin]):
        msg = DexComposer.join_pool(sender, pool_id, tokens)
        return super().execute(msg)

    def exit_pool(self, sender: str, pool_id: int, pool_shares: coin_pb.Coin):
        msg = DexComposer.exit_pool(sender, pool_id, pool_shares)
        return super().execute(msg)

    def swap_assets(self, sender: str, pool_id: int, token_in: coin_pb.Coin, token_out_denom):
        msg = DexComposer.swap_assets(sender, pool_id, token_in, token_out_denom)
        return super().execute(msg)
