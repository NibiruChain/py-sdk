import dataclasses
from datetime import datetime

from nibiru_proto.proto.pricefeed import tx_pb2 as pb

from nibiru.pytypes import PythonMsg
from nibiru.utils import to_sdk_dec, toPbTimestamp


class MsgsPricefeed:
    """
    Messages for the x/pricefeed module.

    Methods:
    - post_price
    """

    @staticmethod
    def post_price(
        oracle: str,
        token0: str,
        token1: str,
        price: float,
        expiry: datetime,
    ) -> 'MsgPostPrice':
        """
        Submits a price from 'oracle' on the specified token pair.

        Attributes:
            oracle (str): address of the msg sender
            token0 (str): base asset denomination, e.g. ATOM
            token1 (str): quote asset denomination, e.g. USD
            price (float): price in units token1 / token0, e.g. price of ATOM in USD.
            expiry (datetime):

        Returns:
            MsgPostPrice: PythonMsg corresponding to 'nibiru.pricefeed.v1.MsgPostPrice'.
        """
        return MsgPostPrice(
            oracle=oracle,
            token0=token0,
            token1=token1,
            price=price,
            expiry=expiry,
        )


@dataclasses.dataclass
class MsgPostPrice(PythonMsg):
    """
    PythonMsg corresponding to 'nibiru.pricefeed.v1.MsgPostPrice'.

    Attributes:
        oracle (str): address of the msg sender
        token0 (str): base asset denomination, e.g. ATOM
        token1 (str): quote asset denomination, e.g. USD
        price (float): price in units token1 / token0, e.g. price of ATOM in USD.
        expiry (datetime):
    """

    oracle: str
    token0: str
    token1: str
    price: float
    expiry: datetime

    def to_pb(self) -> pb.MsgPostPrice:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgPostPrice: The proto object.

        """
        return pb.MsgPostPrice(
            oracle=self.oracle,
            token0=self.token0,
            token1=self.token1,
            price=to_sdk_dec(self.price),
            expiry=toPbTimestamp(self.expiry),
        )
