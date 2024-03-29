"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import cosmos.slashing.v1beta1.slashing_pb2
import google.protobuf.descriptor
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class MsgUnjail(google.protobuf.message.Message):
    """MsgUnjail defines the Msg/Unjail request type"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALIDATOR_ADDR_FIELD_NUMBER: builtins.int
    validator_addr: builtins.str
    def __init__(
        self,
        *,
        validator_addr: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["validator_addr", b"validator_addr"]) -> None: ...

global___MsgUnjail = MsgUnjail

@typing_extensions.final
class MsgUnjailResponse(google.protobuf.message.Message):
    """MsgUnjailResponse defines the Msg/Unjail response type"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___MsgUnjailResponse = MsgUnjailResponse

@typing_extensions.final
class MsgUpdateParams(google.protobuf.message.Message):
    """MsgUpdateParams is the Msg/UpdateParams request type.

    Since: cosmos-sdk 0.47
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    AUTHORITY_FIELD_NUMBER: builtins.int
    PARAMS_FIELD_NUMBER: builtins.int
    authority: builtins.str
    """authority is the address that controls the module (defaults to x/gov unless overwritten)."""
    @property
    def params(self) -> cosmos.slashing.v1beta1.slashing_pb2.Params:
        """params defines the x/slashing parameters to update.

        NOTE: All parameters must be supplied.
        """
    def __init__(
        self,
        *,
        authority: builtins.str = ...,
        params: cosmos.slashing.v1beta1.slashing_pb2.Params | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["params", b"params"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["authority", b"authority", "params", b"params"]) -> None: ...

global___MsgUpdateParams = MsgUpdateParams

@typing_extensions.final
class MsgUpdateParamsResponse(google.protobuf.message.Message):
    """MsgUpdateParamsResponse defines the response structure for executing a
    MsgUpdateParams message.

    Since: cosmos-sdk 0.47
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___MsgUpdateParamsResponse = MsgUpdateParamsResponse
