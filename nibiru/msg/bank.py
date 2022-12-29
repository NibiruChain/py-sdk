import dataclasses
from typing import Iterable, List, Union

from nibiru_proto.proto.cosmos.bank.v1beta1 import tx_pb2 as pb

from nibiru.pytypes import Coin, PythonMsg


class MsgsBank:
    """
    Messages for the x/bank module.

    Methods:
    - send: Send tokens from one account to another
    """

    @staticmethod
    def send(
        from_address: str,
        to_address: str,
        coins: Union[Coin, List[Coin]],
    ) -> 'MsgSend':
        """
        Send tokens from one account to another

        Attributes:
            from_address (str): The address of the sender
            to_address (str): The address of the receiver
            coins (List[Coin]): The list of coins to send

        Returns:
            MsgSend: PythonMsg corresponding to the 'cosmos.bank.v1beta1.MsgSend' message
        """
        return MsgSend(from_address=from_address, to_address=to_address, coins=coins)


@dataclasses.dataclass
class MsgSend(PythonMsg):
    """
    Send tokens from one account to another. PythonMsg corresponding to the
    'cosmos.bank.v1beta1.MsgSend' message.

    Attributes:
        from_address (str): The address of the sender
        to_address (str): The address of the receiver
        coins (Union[Coin, List[Coin]]): The list of coins to send
    """

    from_address: str
    to_address: str
    coins: Union[Coin, List[Coin]]

    def to_pb(self) -> pb.MsgSend:
        """
        Returns the Message as protobuf object.

        Returns:
            pb.MsgSend: The proto object.

        """
        coins = self.coins
        if not isinstance(coins, Iterable):
            coins = [self.coins]

        return pb.MsgSend(
            from_address=self.from_address,
            to_address=self.to_address,
            amount=[coin._generate_proto_object() for coin in coins],
        )
