import abc

import nibiru
import nibiru.msg.bank
import nibiru.msg.dex
import nibiru.msg.perp
import nibiru.msg.pricefeed


class PythonMsg(abc.ABC):
    @abc.abstractmethod
    def to_pb(self) -> nibiru.ProtobufMessage:
        """
        Generate the protobuf message

        Returns:
            Any: The protobuff mesage
        """
