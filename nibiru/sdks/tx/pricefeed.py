from datetime import datetime
import abc
import nibiru
from nibiru.proto.pricefeed import tx_pb2 as pb
from nibiru.sdks.tx.common import BaseTxClient
from dataclasses import dataclass
from typing import Any, List, Sequence, Union
from nibiru.proto.pricefeed import tx_pb2
from nibiru.utils import toTsPb, to_sdk_dec


@dataclass
class MsgPostPrice(nibiru.sdks.PythonMsg):
    oracle: str
    token0: str
    token1: str
    price: float
    expiry: datetime

    def to_pb(self) -> pb.MsgPostPrice:
        self.expiry = toTsPb(self.expiry)

        return pb.MsgPostPrice(
            oracle=self.oracle,
            token0=self.token0,
            token1=self.token1,
            price=to_sdk_dec(self.price),
            expiry=toTsPb(self.expiry),
        )


class PricefeedTxClient(BaseTxClient):
    def post_price(
        self,
        msgs: Union[MsgPostPrice, List[MsgPostPrice]],
        **kwargs,
    ):
        if not isinstance(msgs, list):
            msgs = [msgs]

        return super().execute_msg([msg.to_pb() for msg in msgs], **kwargs)
