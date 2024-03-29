"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import cosmos.upgrade.v1beta1.upgrade_pb2
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
class QueryCurrentPlanRequest(google.protobuf.message.Message):
    """QueryCurrentPlanRequest is the request type for the Query/CurrentPlan RPC
    method.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___QueryCurrentPlanRequest = QueryCurrentPlanRequest

@typing_extensions.final
class QueryCurrentPlanResponse(google.protobuf.message.Message):
    """QueryCurrentPlanResponse is the response type for the Query/CurrentPlan RPC
    method.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PLAN_FIELD_NUMBER: builtins.int
    @property
    def plan(self) -> cosmos.upgrade.v1beta1.upgrade_pb2.Plan:
        """plan is the current upgrade plan."""
    def __init__(
        self,
        *,
        plan: cosmos.upgrade.v1beta1.upgrade_pb2.Plan | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["plan", b"plan"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["plan", b"plan"]) -> None: ...

global___QueryCurrentPlanResponse = QueryCurrentPlanResponse

@typing_extensions.final
class QueryAppliedPlanRequest(google.protobuf.message.Message):
    """QueryCurrentPlanRequest is the request type for the Query/AppliedPlan RPC
    method.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    name: builtins.str
    """name is the name of the applied plan to query for."""
    def __init__(
        self,
        *,
        name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name"]) -> None: ...

global___QueryAppliedPlanRequest = QueryAppliedPlanRequest

@typing_extensions.final
class QueryAppliedPlanResponse(google.protobuf.message.Message):
    """QueryAppliedPlanResponse is the response type for the Query/AppliedPlan RPC
    method.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HEIGHT_FIELD_NUMBER: builtins.int
    height: builtins.int
    """height is the block height at which the plan was applied."""
    def __init__(
        self,
        *,
        height: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["height", b"height"]) -> None: ...

global___QueryAppliedPlanResponse = QueryAppliedPlanResponse

@typing_extensions.final
class QueryUpgradedConsensusStateRequest(google.protobuf.message.Message):
    """QueryUpgradedConsensusStateRequest is the request type for the Query/UpgradedConsensusState
    RPC method.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LAST_HEIGHT_FIELD_NUMBER: builtins.int
    last_height: builtins.int
    """last height of the current chain must be sent in request
    as this is the height under which next consensus state is stored
    """
    def __init__(
        self,
        *,
        last_height: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["last_height", b"last_height"]) -> None: ...

global___QueryUpgradedConsensusStateRequest = QueryUpgradedConsensusStateRequest

@typing_extensions.final
class QueryUpgradedConsensusStateResponse(google.protobuf.message.Message):
    """QueryUpgradedConsensusStateResponse is the response type for the Query/UpgradedConsensusState
    RPC method.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UPGRADED_CONSENSUS_STATE_FIELD_NUMBER: builtins.int
    upgraded_consensus_state: builtins.bytes
    """Since: cosmos-sdk 0.43"""
    def __init__(
        self,
        *,
        upgraded_consensus_state: builtins.bytes = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["upgraded_consensus_state", b"upgraded_consensus_state"]) -> None: ...

global___QueryUpgradedConsensusStateResponse = QueryUpgradedConsensusStateResponse

@typing_extensions.final
class QueryModuleVersionsRequest(google.protobuf.message.Message):
    """QueryModuleVersionsRequest is the request type for the Query/ModuleVersions
    RPC method.

    Since: cosmos-sdk 0.43
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MODULE_NAME_FIELD_NUMBER: builtins.int
    module_name: builtins.str
    """module_name is a field to query a specific module
    consensus version from state. Leaving this empty will
    fetch the full list of module versions from state
    """
    def __init__(
        self,
        *,
        module_name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["module_name", b"module_name"]) -> None: ...

global___QueryModuleVersionsRequest = QueryModuleVersionsRequest

@typing_extensions.final
class QueryModuleVersionsResponse(google.protobuf.message.Message):
    """QueryModuleVersionsResponse is the response type for the Query/ModuleVersions
    RPC method.

    Since: cosmos-sdk 0.43
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MODULE_VERSIONS_FIELD_NUMBER: builtins.int
    @property
    def module_versions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[cosmos.upgrade.v1beta1.upgrade_pb2.ModuleVersion]:
        """module_versions is a list of module names with their consensus versions."""
    def __init__(
        self,
        *,
        module_versions: collections.abc.Iterable[cosmos.upgrade.v1beta1.upgrade_pb2.ModuleVersion] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["module_versions", b"module_versions"]) -> None: ...

global___QueryModuleVersionsResponse = QueryModuleVersionsResponse

@typing_extensions.final
class QueryAuthorityRequest(google.protobuf.message.Message):
    """QueryAuthorityRequest is the request type for Query/Authority

    Since: cosmos-sdk 0.46
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___QueryAuthorityRequest = QueryAuthorityRequest

@typing_extensions.final
class QueryAuthorityResponse(google.protobuf.message.Message):
    """QueryAuthorityResponse is the response type for Query/Authority

    Since: cosmos-sdk 0.46
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ADDRESS_FIELD_NUMBER: builtins.int
    address: builtins.str
    def __init__(
        self,
        *,
        address: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["address", b"address"]) -> None: ...

global___QueryAuthorityResponse = QueryAuthorityResponse
