"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import cosmos.app.v1alpha1.config_pb2
import google.protobuf.descriptor
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class QueryConfigRequest(google.protobuf.message.Message):
    """QueryConfigRequest is the Query/Config request type."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___QueryConfigRequest = QueryConfigRequest

@typing_extensions.final
class QueryConfigResponse(google.protobuf.message.Message):
    """QueryConfigRequest is the Query/Config response type."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONFIG_FIELD_NUMBER: builtins.int
    @property
    def config(self) -> cosmos.app.v1alpha1.config_pb2.Config:
        """config is the current app config."""
    def __init__(
        self,
        *,
        config: cosmos.app.v1alpha1.config_pb2.Config | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["config", b"config"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["config", b"config"]) -> None: ...

global___QueryConfigResponse = QueryConfigResponse
