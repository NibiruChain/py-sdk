"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
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
class GenesisState(google.protobuf.message.Message):
    """GenesisState defines the slashing module's genesis state."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PARAMS_FIELD_NUMBER: builtins.int
    SIGNING_INFOS_FIELD_NUMBER: builtins.int
    MISSED_BLOCKS_FIELD_NUMBER: builtins.int
    @property
    def params(self) -> cosmos.slashing.v1beta1.slashing_pb2.Params:
        """params defines all the parameters of the module."""
    @property
    def signing_infos(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___SigningInfo]:
        """signing_infos represents a map between validator addresses and their
        signing infos.
        """
    @property
    def missed_blocks(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ValidatorMissedBlocks]:
        """missed_blocks represents a map between validator addresses and their
        missed blocks.
        """
    def __init__(
        self,
        *,
        params: cosmos.slashing.v1beta1.slashing_pb2.Params | None = ...,
        signing_infos: collections.abc.Iterable[global___SigningInfo] | None = ...,
        missed_blocks: collections.abc.Iterable[global___ValidatorMissedBlocks] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["params", b"params"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["missed_blocks", b"missed_blocks", "params", b"params", "signing_infos", b"signing_infos"]) -> None: ...

global___GenesisState = GenesisState

@typing_extensions.final
class SigningInfo(google.protobuf.message.Message):
    """SigningInfo stores validator signing info of corresponding address."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ADDRESS_FIELD_NUMBER: builtins.int
    VALIDATOR_SIGNING_INFO_FIELD_NUMBER: builtins.int
    address: builtins.str
    """address is the validator address."""
    @property
    def validator_signing_info(self) -> cosmos.slashing.v1beta1.slashing_pb2.ValidatorSigningInfo:
        """validator_signing_info represents the signing info of this validator."""
    def __init__(
        self,
        *,
        address: builtins.str = ...,
        validator_signing_info: cosmos.slashing.v1beta1.slashing_pb2.ValidatorSigningInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["validator_signing_info", b"validator_signing_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["address", b"address", "validator_signing_info", b"validator_signing_info"]) -> None: ...

global___SigningInfo = SigningInfo

@typing_extensions.final
class ValidatorMissedBlocks(google.protobuf.message.Message):
    """ValidatorMissedBlocks contains array of missed blocks of corresponding
    address.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ADDRESS_FIELD_NUMBER: builtins.int
    MISSED_BLOCKS_FIELD_NUMBER: builtins.int
    address: builtins.str
    """address is the validator address."""
    @property
    def missed_blocks(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___MissedBlock]:
        """missed_blocks is an array of missed blocks by the validator."""
    def __init__(
        self,
        *,
        address: builtins.str = ...,
        missed_blocks: collections.abc.Iterable[global___MissedBlock] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["address", b"address", "missed_blocks", b"missed_blocks"]) -> None: ...

global___ValidatorMissedBlocks = ValidatorMissedBlocks

@typing_extensions.final
class MissedBlock(google.protobuf.message.Message):
    """MissedBlock contains height and missed status as boolean."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INDEX_FIELD_NUMBER: builtins.int
    MISSED_FIELD_NUMBER: builtins.int
    index: builtins.int
    """index is the height at which the block was missed."""
    missed: builtins.bool
    """missed is the missed status."""
    def __init__(
        self,
        *,
        index: builtins.int = ...,
        missed: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["index", b"index", "missed", b"missed"]) -> None: ...

global___MissedBlock = MissedBlock
