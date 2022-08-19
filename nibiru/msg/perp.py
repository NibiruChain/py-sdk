import dataclasses

from nibiru_proto.proto.perp.v1 import state_pb2 as state_pb
from nibiru_proto.proto.perp.v1 import tx_pb2 as pb

from nibiru.common import Coin, PythonMsg, Side
from nibiru.utils import to_sdk_dec, to_sdk_int


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
        return pb.MsgAddMargin(
            sender=self.sender,
            token_pair=self.token_pair,
            margin=self.margin._generate_proto_object(),
        )


@dataclasses.dataclass
class MsgOpenPosition(PythonMsg):
    """
    Open a posiiton using the specified parameters.

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
