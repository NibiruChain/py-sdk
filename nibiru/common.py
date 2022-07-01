from enum import Enum
from dataclasses import dataclass
from nibiru.proto.cosmos.base.v1beta1 import coin_pb2 as coin_pb

class Side(Enum):
    BUY = 1
    SELL = 2

@dataclass
class PoolAsset:
    token: coin_pb.Coin
    weight: str
