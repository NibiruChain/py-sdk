import dataclasses
from datetime import datetime
from typing import List, Union

from nibiru_proto.proto.pricefeed import tx_pb2 as pb

import nibiru
from nibiru.sdks.tx.common import BaseTxClient
from nibiru.utils import to_sdk_dec, toPbTimestamp


@dataclasses.dataclass
class MsgPostPrice(nibiru.sdks.PythonMsg):
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


class PricefeedTxClient(BaseTxClient):
    """
    Methods:
        post_price (Callable[[msgs, **kwargs], TxResponse])
    """

    def post_price(
        self,
        msgs: Union[MsgPostPrice, List[MsgPostPrice]],
        **kwargs,
    ):
        if not isinstance(msgs, list):
            msgs = [msgs]

        pb_msgs: List[MsgPostPrice] = []
        for msg in msgs:
            if not isinstance(msg, MsgPostPrice):
                raise TypeError(f"Invalid type for msgs: {type(msg)}")
            pb_msgs.append(msg.to_pb())
        # return super(PricefeedTxClient, self).execute_msg(pb_msgs, **kwargs)
        return super().execute_msgs(pb_msgs, **kwargs)
