from datetime import datetime

from nibiru import utils
from nibiru.proto.pricefeed import tx_pb2 as pb
from nibiru.sdks.tx.common import BaseTxClient


class PricefeedTxClient(BaseTxClient):
    def post_price(
        self,
        oracle: str,
        token0: str,
        token1: str,
        price: float,
        expiry: datetime,
        **kwargs,
    ):
        price_dec = utils.to_sdk_dec(price)
        msg = pb.MsgPostPrice(
            oracle=oracle,
            token0=token0,
            token1=token1,
            price=price_dec,
            expiry=utils.toTsPb(expiry),
        )
        return super().execute_msg(msg, **kwargs)
