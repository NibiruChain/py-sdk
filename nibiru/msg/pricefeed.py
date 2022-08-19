import dataclasses
from datetime import datetime

from nibiru_proto.proto.pricefeed import tx_pb2 as pb

from nibiru.common import PythonMsg
from nibiru.utils import to_sdk_dec, toPbTimestamp


@dataclasses.dataclass
class MsgPostPrice(PythonMsg):
    """
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
        return pb.MsgPostPrice(
            oracle=self.oracle,
            token0=self.token0,
            token1=self.token1,
            price=to_sdk_dec(self.price),
            expiry=toPbTimestamp(self.expiry),
        )
