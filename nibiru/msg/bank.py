import dataclasses
from typing import Iterable, List, Union

from nibiru_proto.proto.cosmos.bank.v1beta1 import tx_pb2 as pb
from nibiru_proto.proto.cosmos.distribution.v1beta1 import tx_pb2 as tx_pb
from nibiru_proto.proto.cosmos.staking.v1beta1 import tx_pb2 as staking_pb

from nibiru.common import Coin, PythonMsg


@dataclasses.dataclass
class MsgSend(PythonMsg):
    """
    Send tokens from one account to another

    Attributes:
        from_address (str): The address of the sender
        to_address (str): The address of the receiver
        coins (List[Coin]): The list of coins to send
    """

    from_address: str
    to_address: str
    coins: Union[Coin, List[Coin]]

    def to_pb(self) -> pb.MsgSend:
        coins = self.coins
        if not isinstance(coins, Iterable):
            coins = [self.coins]

        return pb.MsgSend(
            from_address=self.from_address,
            to_address=self.to_address,
            amount=[coin._generate_proto_object() for coin in coins],
        )


@dataclasses.dataclass
class MsgDelegate(PythonMsg):
    """
    Delegate tokens to a validator

    Attributes:
        delegator_address: str
        validator_address: str
        amount: float
    """

    delegator_address: str
    validator_address: str
    amount: float

    def to_pb(self) -> staking_pb.MsgDelegate:
        return staking_pb.MsgDelegate(
            delegator_address=self.delegator_address,
            validator_address=self.validator_address,
            amount=Coin(self.amount, "unibi"),
        )


@dataclasses.dataclass
class MsgWithdrawDelegatorReward(PythonMsg):
    """
    Withdraw the reward from a validator

    Attributes:
        delegator_address: str
        validator_address: str
    """

    delegator_address: str
    validator_address: str

    def to_pb(self) -> tx_pb.MsgWithdrawDelegatorReward:
        return tx_pb.MsgWithdrawDelegatorReward(
            delegator_address=self.delegator_address,
            validator_address=self.validator_address,
        )
