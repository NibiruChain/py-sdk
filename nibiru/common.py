from enum import Enum
from dataclasses import dataclass
from .proto.cosmos.base.v1beta1 import coin_pb2 as coin_pb

class Side(Enum):
    BUY = 1
    SELL = 2

@dataclass
class PoolAsset:
    token: coin_pb.Coin
    weight: str

class TxConfig:
    def __init__(self, gas_wanted: int = 0, gas_multiplier: float = 0, gas_price: float = 0):
        '''
        Parameters:
            gas_wanted (int): Set the absolute gas_wanted to be used
            gas_multiplier (float): Set the gas multiplier that's being applied to the estimated gas, defaults to 1.25.
                                    If gas_wanted is set this property is ignored.
            gas_price(float): Set the gas price used to calculate the fee
        '''
        self.gas_multiplier = gas_multiplier
        self.gas_wanted = gas_wanted
        self.gas_price = gas_price
