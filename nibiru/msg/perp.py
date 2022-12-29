import dataclasses

from nibiru_proto.proto.perp.v1 import state_pb2 as state_pb
from nibiru_proto.proto.perp.v1 import tx_pb2 as pb

from nibiru.pytypes import Coin, PythonMsg, Side
from nibiru.utils import to_sdk_dec, to_sdk_int


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
        sender: str,
        token_pair: str,
        is_long: bool,
        quote_asset_amount: float,
        leverage: float,
        base_asset_amount_limit: float,
    ) -> 'MsgOpenPosition':
        """
        Open a posiiton using the specified parameters.

        Attributes:
            sender (str): The sender address
            token_pair (str): The token pair
            is_long (bool): Determines whether to open with long or short exposure.
            quote_asset_amount (float): The quote amount you want to use to buy base
            leverage (float): The leverage you want to use, typically between 1 and 15, depending on the maintenance
                margin ratio of the pool.
            base_asset_amount_limit (float): The minimum amount of base you are willing to receive for this amount of
                quote.
        """
        side: Side
        if is_long:
            side = Side.BUY
        else:
            side = Side.SELL
        return MsgOpenPosition(
            sender=sender,
            token_pair=token_pair,
            side=side,
            quote_asset_amount=quote_asset_amount,
            leverage=leverage,
            base_asset_amount_limit=base_asset_amount_limit,
        )

    @staticmethod
    def close_position(
        sender: str,
        token_pair: str,
    ) -> 'MsgClosePosition':
        """
        Close the position.

        Attributes:
            sender (str): The sender address
            token_pair (str): The token pair
        """
        return MsgClosePosition(sender=sender, token_pair=token_pair)

    @staticmethod
    def add_margin(
        sender: str,
        token_pair: str,
        margin: Coin,
    ) -> 'MsgAddMargin':
        """
        Add margin for the position (token_pair + trader)

        Attributes:
            sender (str): The trader address
            token_pair (str): The token pair
            margin (Coin): The margin to remove in a coin format
        """
        return MsgAddMargin(sender=sender, token_pair=token_pair, margin=margin)

    @staticmethod
    def remove_margin(
        sender: str,
        token_pair: str,
        margin: Coin,
    ) -> 'MsgRemoveMargin':
        """
        Remove margin for the position (token_pair + trader)

        Attributes:
            sender (str): The trader address
            token_pair (str): The token pair
            margin (Coin): The margin to remove in a coin format
        """
        return MsgRemoveMargin(sender=sender, token_pair=token_pair, margin=margin)

    @staticmethod
    def liquidate(
        sender: str,
        token_pair: str,
        trader: str,
    ) -> 'MsgLiquidate':
        """
        Liquidates unhealthy position (token_pair + trader)

        Attributes:
            sender (str): The liquidator address
            token_pair (str): The token pair
            trader (str): The trader address
        """
        return MsgLiquidate(sender=sender, token_pair=token_pair, trader=trader)


@dataclasses.dataclass
class MsgRemoveMargin(PythonMsg):
    """
    Remove margin for the position (token_pair + trader)

    Attributes:
        sender (str): The trader address
        token_pair (str): The token pair
        margin (Coin): The margin to remove in a coin format
    """

    sender: str
    token_pair: str
    margin: Coin

    def to_pb(self) -> pb.MsgRemoveMargin:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgRemoveMargin: The proto object.

        """
        return pb.MsgRemoveMargin(
            sender=self.sender,
            token_pair=self.token_pair,
            margin=self.margin._generate_proto_object(),
        )


@dataclasses.dataclass
class MsgAddMargin(PythonMsg):
    """
    Add margin for the position (token_pair + trader)

    Attributes:
        sender (str): The trader address
        token_pair (str): The token pair
        margin (Coin): The margin to remove in a coin format
    """

    sender: str
    token_pair: str
    margin: Coin

    def to_pb(self) -> pb.MsgAddMargin:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgAddMargin: The proto object.

        """
        return pb.MsgAddMargin(
            sender=self.sender,
            token_pair=self.token_pair,
            margin=self.margin._generate_proto_object(),
        )


@dataclasses.dataclass
class MsgOpenPosition(PythonMsg):
    """
    Open a position using the specified parameters.

    Attributes:
        sender (str): The sender address
        token_pair (str): The token pair
        side (Side): The side, either Side.BUY or Side.SELL
        quote_asset_amount (float): The quote amount you want to use to buy base
        leverage (float): The leverage you want to use, typically between 1 and 15, depending on the maintenance
            margin ratio of the pool.
        base_asset_amount_limit (float): The minimum amount of base you are willing to receive for this amount of
            quote.
    """

    sender: str
    token_pair: str
    side: Side
    quote_asset_amount: float
    leverage: float
    base_asset_amount_limit: float

    def to_pb(self) -> pb.MsgOpenPosition:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgOpenPosition: The proto object.

        """
        pb_side = state_pb.Side.BUY if self.side == Side.BUY else state_pb.SELL
        quote_asset_amount_pb = to_sdk_int(self.quote_asset_amount)
        base_asset_amount_limit_pb = to_sdk_int(self.base_asset_amount_limit)
        leverage_pb = to_sdk_dec(self.leverage)

        return pb.MsgOpenPosition(
            sender=self.sender,
            token_pair=self.token_pair,
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
        sender (str): The sender address
        token_pair (str): The token pair
    """

    sender: str
    token_pair: str

    def to_pb(self) -> pb.MsgClosePosition:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgClosePosition: The proto object.

        """
        return pb.MsgClosePosition(
            sender=self.sender,
            token_pair=self.token_pair,
        )


@dataclasses.dataclass
class MsgLiquidate(PythonMsg):
    """
    Close the position.

    Attributes:
        sender (str): The sender address
        token_pair (str): The token pair
    """

    sender: str
    token_pair: str
    trader: str

    def to_pb(self) -> pb.MsgLiquidate:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgLiquidate: The proto object.

        """
        return pb.MsgLiquidate(
            sender=self.sender,
            token_pair=self.token_pair,
            trader=self.trader,
        )


class perp:
    """
    The perp class allows you to generate transaction for the perpetual futures module using the different messages
    available.
    """

    remove_margin: MsgRemoveMargin
    add_margin: MsgAddMargin
    open_position: MsgOpenPosition
    close_position: MsgClosePosition
    liquidate: MsgLiquidate
