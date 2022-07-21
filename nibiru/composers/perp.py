from nibiru.common import Side
from nibiru.proto.cosmos.base.v1beta1 import coin_pb2 as coin_pb
from nibiru.proto.perp.v1 import state_pb2 as state_pb
from nibiru.proto.perp.v1 import tx_pb2 as tx
from nibiru.utils import float_to_sdkdec, float_to_sdkint


class Perp:
    @staticmethod
    def remove_margin(sender: str, token_pair: str, margin: coin_pb.Coin):
        return tx.MsgRemoveMargin(
            sender=sender,
            token_pair=token_pair,
            margin=margin,
        )

    @staticmethod
    def add_margin(sender: str, token_pair: str, margin: coin_pb.Coin):
        return tx.MsgAddMargin(
            sender=sender,
            token_pair=token_pair,
            margin=margin,
        )

    @staticmethod
    def liquidate(sender: str, token_pair: str, trader: str):
        return tx.MsgLiquidate(
            sender=sender,
            token_pair=token_pair,
            trader=trader,
        )

    @staticmethod
    def open_position(
        sender: str,
        token_pair: str,
        side: Side,
        quote_asset_amount: float,
        leverage: float,
        base_asset_amount_limit: float,
    ):
        pb_side = state_pb.Side.BUY if side == Side.BUY else state_pb.SELL
        quote_asset_amount_pb = float_to_sdkint(quote_asset_amount)
        base_asset_amount_limit_pb = float_to_sdkint(base_asset_amount_limit)
        leverage_pb = float_to_sdkdec(leverage)
        return tx.MsgOpenPosition(
            sender=sender,
            token_pair=token_pair,
            side=pb_side,
            quote_asset_amount=quote_asset_amount_pb,
            leverage=leverage_pb,
            base_asset_amount_limit=base_asset_amount_limit_pb,
        )

    @staticmethod
    def close_position(sender: str, token_pair: str):
        return tx.MsgClosePosition(
            sender=sender,
            token_pair=token_pair,
        )
