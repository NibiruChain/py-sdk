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
