import abc

import nibiru


class PythonMsg(abc.ABC):
    @abc.abstractmethod
    def to_pb(self) -> nibiru.ProtobufMessage:
        """
        Generate the protobuf message

        Returns:
            Any: The protobuff mesage
        """


from nibiru.msg.bank import MsgDelegate, MsgSend, MsgWithdrawDelegatorReward  # noqa
from nibiru.msg.dex import (  # noqa
    MsgCreatePool,
    MsgExitPool,
    MsgJoinPool,
    MsgSwapAssets,
)
from nibiru.msg.perp import (  # noqa
    MsgAddMargin,
    MsgClosePosition,
    MsgLiquidate,
    MsgOpenPosition,
    MsgRemoveMargin,
)
from nibiru.msg.pricefeed import MsgPostPrice  # noqa
