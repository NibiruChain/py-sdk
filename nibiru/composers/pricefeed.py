from datetime import datetime

from nibiru import utils
from nibiru.proto.pricefeed import tx_pb2 as pb


class Pricefeed:
    @staticmethod
    def post_price(oracle: str, token0: str, token1: str, price: float, expiry: datetime):
        price_dec = utils.float_to_sdkdec(price)
        return pb.MsgPostPrice(
            oracle=oracle,
            token0=token0,
            token1=token1,
            price=price_dec,
            expiry=utils.toTsPb(expiry),
        )
