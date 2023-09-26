import dataclasses
from typing import List

from nibiru.pytypes import Coin, Direction, PythonMsg
from nibiru.utils import to_sdk_dec, to_sdk_int
from nibiru_proto.nibiru.perp.v2 import state_pb2 as state_pb
from nibiru_proto.nibiru.perp.v2 import tx_pb2 as pb


@dataclasses.dataclass
class Liquidation:
    """
    Keeper of the pair/trader pairs for liquidations
    """

    pair: str
    trader: str


class MsgsPerp:
    """
    Messages for the Nibiru Chain x/perp module

    Methods:
    - open_position
    - close_position:
    - add_margin: Deleverages a position by adding margin to back it.
    - remove_margin: Increases the leverage of the position by removing margin.
    """

    @staticmethod
    def open_position(
        pair: str,
        is_long: bool,
        quote_asset_amount: float,
        leverage: float,
        base_asset_amount_limit: float,
    ) -> 'MsgMarketOrder':
        """
        Open a posiiton using the specified parameters.

        Attributes:
            pair (str): The token pair
            is_long (bool): Determines whether to open with long or short exposure.
            quote_asset_amount (float): The quote amount you want to use to buy base
            leverage (float): The leverage you want to use, typically between 1 and 15, depending on the maintenance
                margin ratio of the pool.
            base_asset_amount_limit (float): The minimum amount of base you are willing to receive for this amount of
                quote.
        """
        return MsgMarketOrder(
            pair=pair,
            dir=Direction.LONG if is_long else Direction.SHORT,
            quote_asset_amount=quote_asset_amount,
            leverage=leverage,
            base_asset_amount_limit=base_asset_amount_limit,
        )

    @staticmethod
    def close_position(pair: str) -> 'MsgClosePosition':
        """
        Close the position.

        Attributes:
            pair (str): The token pair
        """
        return MsgClosePosition(pair=pair)

    @staticmethod
    def add_margin(
        pair: str,
        margin: Coin,
    ) -> 'MsgAddMargin':
        """
        Add margin for the position (pair + trader)

        Attributes:
            pair (str): The token pair
            margin (Coin): The margin to remove in a coin format
        """
        return MsgAddMargin(pair=pair, margin=margin)

    @staticmethod
    def remove_margin(pair: str, margin: Coin) -> 'MsgRemoveMargin':
        """
        Remove margin for the position (pair + trader)

        Attributes:
            pair (str): The token pair
            margin (Coin): The margin to remove in a coin format
        """
        return MsgRemoveMargin(pair=pair, margin=margin)

    @staticmethod
    def liquidate(pair: str, trader: str) -> 'MsgMultiLiquidate':
        """
        Liquidates unhealthy position (pair + trader)

        Attributes:
            pair (str): The token pair
            trader (str): The trader address
        """
        return MsgMultiLiquidate(liquidations=[Liquidation(pair=pair, trader=trader)])

    @staticmethod
    def liquidate_multiple(liquidations: List[Liquidation]) -> 'MsgMultiLiquidate':
        """
        Liquidates multiple unhealthy positions (pair + trader)

        Attributes:
            liquidations (List[Liquidation]): list of pair/traders to liquidate
        """
        return MsgMultiLiquidate(liquidations=liquidations)


@dataclasses.dataclass
class MsgRemoveMargin(PythonMsg):
    """
    Remove margin for the position (pair + trader)

    Attributes:
        pair (str): The token pair
        margin (Coin): The margin to remove in a coin format
    """

    pair: str
    margin: Coin

    def to_pb(self, sender: str) -> pb.MsgRemoveMargin:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgRemoveMargin: The proto object.

        """
        return pb.MsgRemoveMargin(
            sender=sender,
            pair=self.pair,
            margin=self.margin.to_pb(),
        )


@dataclasses.dataclass
class MsgAddMargin(PythonMsg):
    """
    Add margin for the position (pair + trader)

    Attributes:
        pair (str): The token pair
        margin (Coin): The margin to remove in a coin format
    """

    pair: str
    margin: Coin

    def to_pb(self, sender: str) -> pb.MsgAddMargin:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgAddMargin: The proto object.

        """
        return pb.MsgAddMargin(
            sender=sender,
            pair=self.pair,
            margin=self.margin.to_pb(),
        )


@dataclasses.dataclass
class MsgMarketOrder(PythonMsg):
    """
    Open a position using the specified parameters.

    Attributes:
        pair (str): The token pair
        side (Side): The side, either Side.BUY or Side.SELL
        quote_asset_amount (float): The quote amount you want to use to buy base
        leverage (float): The leverage you want to use, typically between 1 and 15, depending on the maintenance
            margin ratio of the pool.
        base_asset_amount_limit (float): The minimum amount of base you are willing to receive for this amount of
            quote.
    """

    pair: str
    dir: Direction
    quote_asset_amount: float
    leverage: float
    base_asset_amount_limit: float

    def to_pb(self, sender: str) -> pb.MsgMarketOrder:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgMarketOrder: The proto object.

        """
        pb_side = (
            state_pb.Direction.LONG
            if self.dir == Direction.LONG
            else state_pb.Direction.SHORT
        )
        quote_asset_amount_pb = to_sdk_int(self.quote_asset_amount)
        base_asset_amount_limit_pb = to_sdk_int(self.base_asset_amount_limit)
        leverage_pb = to_sdk_dec(self.leverage)

        return pb.MsgMarketOrder(
            sender=sender,
            pair=self.pair,
            side=pb_side,
            quote_asset_amount=quote_asset_amount_pb,
            leverage=leverage_pb,
            base_asset_amount_limit=base_asset_amount_limit_pb,
        )


@dataclasses.dataclass
class MsgClosePosition(PythonMsg):
    """
    Close the position.

    Attributes:
        pair (str): The token pair
    """

    pair: str

    def to_pb(self, sender: str) -> pb.MsgClosePosition:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgClosePosition: The proto object.

        """
        return pb.MsgClosePosition(
            sender=sender,
            pair=self.pair,
        )


@dataclasses.dataclass
class MsgMultiLiquidate(PythonMsg):
    """
    Liquidate one or multiple unhealthy positions.
    Unhealthy positions are positions with margin_ratio < maintenance_margin_ratio.

    Attributes:
        liquidations (Liquidation): The list of {pair, trader} pairs.
    """

    liquidations: List[Liquidation]

    def to_pb(self, sender: str) -> pb.MsgMultiLiquidate:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgLiquidate: The proto object.

        """
        return pb.MsgMultiLiquidate(
            sender=sender,
            liquidations=[
                pb.MsgMultiLiquidate.Liquidation(
                    pair=liquidation.pair,
                    trader=liquidation.trader,
                )
                for liquidation in self.liquidations
            ],
        )


class perp:
    """
    The perp class allows you to generate transaction for the perpetual futures module
    using the different messages available.
    """

    remove_margin: MsgRemoveMargin
    add_margin: MsgAddMargin
    open_position: MsgMarketOrder
    close_position: MsgClosePosition
    liquidate: MsgMultiLiquidate
