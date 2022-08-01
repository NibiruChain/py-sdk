from dataclasses import dataclass
from enum import Enum

from .proto.cosmos.base.v1beta1 import coin_pb2 as coin_pb
from .proto.cosmos.base.v1beta1 import coin_pb2 as cosmos_base_coin_pb

class TxType(Enum):
    SYNC = 1
    ASYNC = 2
    BLOCK = 3


class Side(Enum):
    BUY = 1
    SELL = 2


class Direction(Enum):
    ADD = 1
    REMOVE = 2

@dataclass
class Coin:
    amount: float
    denom: str

    def _generate_proto_object(self):
        return cosmos_base_coin_pb.Coin(amount=str(self.amount), denom=self.denom)

@dataclass
class PoolAsset:
    token: Coin
    weight: float


class TxConfig:
    def __init__(
        self, gas_wanted: int = 0, gas_multiplier: float = 0, gas_price: float = 0, tx_type: TxType = TxType.ASYNC
    ):
        '''
        Parameters:
            gas_wanted (int): Set the absolute gas_wanted to be used
            gas_multiplier (float): Set the gas multiplier that's being applied to the estimated gas, defaults to 1.25.
                                    If gas_wanted is set this property is ignored.
            gas_price(float): Set the gas price used to calculate the fee
            tx_type (TxType): Configure how to execute the tx, defaults to `ASYNC`
        '''
        self.gas_multiplier = gas_multiplier
        self.gas_wanted = gas_wanted
        self.gas_price = gas_price
        self.tx_type = tx_type
