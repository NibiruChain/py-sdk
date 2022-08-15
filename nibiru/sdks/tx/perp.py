from nibiru.common import Coin, Side
from nibiru.proto.perp.v1 import state_pb2 as state_pb
from nibiru.proto.perp.v1 import tx_pb2 as tx
from nibiru.sdks.tx.common import BaseTxClient
from nibiru.utils import to_sdk_dec, to_sdk_int


class PerpTxClient(BaseTxClient):
    def remove_margin(self, sender: str, token_pair: str, margin: Coin, **kwargs):
        """
        Remove margin for the position (token_pair + trader)

        Args:
            sender (str): The trader address
            token_pair (str): The token pair
            margin (Coin): The margin to remove in a coin format

        Returns:
            str: The output of the transaction
        """
        msg = tx.MsgRemoveMargin(
            sender=sender,
            token_pair=token_pair,
            margin=margin._generate_proto_object(),
        )
        return super().execute_msg(msg, **kwargs)

    def add_margin(self, sender: str, token_pair: str, margin: Coin, **kwargs):
        """
        Add margin for the position (token_pair + trader)

        Args:
            sender (str): The trader address
            token_pair (str): The token pair
            margin (Coin): The margin to add in a coin format

        Returns:
            str: The output of the transaction
        """
        msg = tx.MsgAddMargin(
            sender=sender,
            token_pair=token_pair,
            margin=margin._generate_proto_object(),
        )
        return super().execute_msg(msg, **kwargs)

    def liquidate(self, sender: str, token_pair: str, trader: str, **kwargs):
        """
        Send a liquidate transaction for the specified trader. You need a whitelisted address to be able to liquidate
        other traders.

        Args:
            sender (str): The address of the account sending the transaction
            token_pair (str): The token pair
            trader (str): The trader address

        Returns:
            str: The output of the transaction
        """
        msg = tx.MsgLiquidate(
            sender=sender,
            token_pair=token_pair,
            trader=trader,
        )
        return super().execute_msg(msg, **kwargs)

    def open_position(
        self,
        sender: str,
        token_pair: str,
        side: Side,
        quote_asset_amount: float,
        leverage: float,
        base_asset_amount_limit: float,
        **kwargs,
    ):
        """
        Open a posiiton using the specified parameters.

        Args:
            sender (str): The sender address
            token_pair (str): The token pair
            side (Side): The side, either Side.BUY or Side.SELL
            quote_asset_amount (float): The quote amount you want to use to buy base
            leverage (float): The leverage you want to use, typically between 1 and 15, depending on the maintenance
                margin ratio of the pool.
            base_asset_amount_limit (float): The minimum amount of base you are willing to receive for this amount of
                quote.

        Returns:
            str: The output of the transaction
        """

        pb_side = state_pb.Side.BUY if side == Side.BUY else state_pb.SELL
        quote_asset_amount_pb = to_sdk_int(quote_asset_amount)
        base_asset_amount_limit_pb = to_sdk_int(base_asset_amount_limit)
        leverage_pb = to_sdk_dec(leverage)

        msg = tx.MsgOpenPosition(
            sender=sender,
            token_pair=token_pair,
            side=pb_side,
            quote_asset_amount=quote_asset_amount_pb,
            leverage=leverage_pb,
            base_asset_amount_limit=base_asset_amount_limit_pb,
        )
        return super().execute_msg(msg, **kwargs)

    def close_position(self, sender: str, token_pair: str, **kwargs):
        """
        Close the position.

        Args:
            sender (str): The sender address
            token_pair (str): The token pair

        Returns:
            str: The output of the transaction
        """
        msg = tx.MsgClosePosition(
            sender=sender,
            token_pair=token_pair,
        )
        return super().execute_msg(msg, **kwargs)
