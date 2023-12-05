"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import cosmos.base.query.v1beta1.pagination_pb2
import cosmos.slashing.v1beta1.slashing_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class QueryParamsRequest(google.protobuf.message.Message):
    """QueryParamsRequest is the request type for the Query/Params RPC method"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___QueryParamsRequest = QueryParamsRequest

@typing_extensions.final
class QueryParamsResponse(google.protobuf.message.Message):
    """QueryParamsResponse is the response type for the Query/Params RPC method"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PARAMS_FIELD_NUMBER: builtins.int
    @property
    def params(self) -> cosmos.slashing.v1beta1.slashing_pb2.Params: ...
    def __init__(
        self,
        *,
        params: cosmos.slashing.v1beta1.slashing_pb2.Params | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["params", b"params"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["params", b"params"]) -> None: ...

global___QueryParamsResponse = QueryParamsResponse

@typing_extensions.final
class QuerySigningInfoRequest(google.protobuf.message.Message):
    """QuerySigningInfoRequest is the request type for the Query/SigningInfo RPC
    method
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONS_ADDRESS_FIELD_NUMBER: builtins.int
    cons_address: builtins.str
    """cons_address is the address to query signing info of"""
    def __init__(
        self,
        *,
        cons_address: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["cons_address", b"cons_address"]) -> None: ...

global___QuerySigningInfoRequest = QuerySigningInfoRequest

@typing_extensions.final
class QuerySigningInfoResponse(google.protobuf.message.Message):
    """QuerySigningInfoResponse is the response type for the Query/SigningInfo RPC
    method
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VAL_SIGNING_INFO_FIELD_NUMBER: builtins.int
    @property
    def val_signing_info(self) -> cosmos.slashing.v1beta1.slashing_pb2.ValidatorSigningInfo:
        """val_signing_info is the signing info of requested val cons address"""
    def __init__(
        self,
        *,
        val_signing_info: cosmos.slashing.v1beta1.slashing_pb2.ValidatorSigningInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["val_signing_info", b"val_signing_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["val_signing_info", b"val_signing_info"]) -> None: ...

global___QuerySigningInfoResponse = QuerySigningInfoResponse

@typing_extensions.final
class QuerySigningInfosRequest(google.protobuf.message.Message):
    """QuerySigningInfosRequest is the request type for the Query/SigningInfos RPC
    method
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PAGINATION_FIELD_NUMBER: builtins.int
    @property
    def pagination(self) -> cosmos.base.query.v1beta1.pagination_pb2.PageRequest: ...
    def __init__(
        self,
        *,
        pagination: cosmos.base.query.v1beta1.pagination_pb2.PageRequest | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["pagination", b"pagination"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["pagination", b"pagination"]) -> None: ...

global___QuerySigningInfosRequest = QuerySigningInfosRequest

@typing_extensions.final
class QuerySigningInfosResponse(google.protobuf.message.Message):
    """QuerySigningInfosResponse is the response type for the Query/SigningInfos RPC
    method
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INFO_FIELD_NUMBER: builtins.int
    PAGINATION_FIELD_NUMBER: builtins.int
    @property
    def info(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[cosmos.slashing.v1beta1.slashing_pb2.ValidatorSigningInfo]:
        """info is the signing info of all validators"""
    @property
    def pagination(self) -> cosmos.base.query.v1beta1.pagination_pb2.PageResponse: ...
    def __init__(
        self,
        *,
        info: collections.abc.Iterable[cosmos.slashing.v1beta1.slashing_pb2.ValidatorSigningInfo] | None = ...,
        pagination: cosmos.base.query.v1beta1.pagination_pb2.PageResponse | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["pagination", b"pagination"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["info", b"info", "pagination", b"pagination"]) -> None: ...

global___QuerySigningInfosResponse = QuerySigningInfosResponse