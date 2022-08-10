from datetime import datetime

from nibiru.composers import Pricefeed as PricefeedComposer

from .common import Tx


class Pricefeed(Tx):
    def post_price(self, oracle: str, token0: str, token1: str, price: float, expiry: datetime, **kwargs):
        msg = PricefeedComposer.post_price(oracle, token0, token1, price, expiry)
        return super().execute_msg(msg, **kwargs)
