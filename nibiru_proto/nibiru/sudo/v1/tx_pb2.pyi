"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
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
class MsgEditSudoers(google.protobuf.message.Message):
    """-------------------------- EditSudoers --------------------------

    MsgEditSudoers: Msg to update the "Sudoers" state.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ACTION_FIELD_NUMBER: builtins.int
    CONTRACTS_FIELD_NUMBER: builtins.int
    SENDER_FIELD_NUMBER: builtins.int
    action: builtins.str
    """Action: identifier for the type of edit that will take place. Using this
      action field prevents us from needing to create several similar message
      types.
    """
    @property
    def contracts(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Contracts: An input payload."""
    sender: builtins.str
    """Sender: Address for the signer of the transaction."""
    def __init__(
        self,
        *,
        action: builtins.str = ...,
        contracts: collections.abc.Iterable[builtins.str] | None = ...,
        sender: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["action", b"action", "contracts", b"contracts", "sender", b"sender"]) -> None: ...

global___MsgEditSudoers = MsgEditSudoers

@typing_extensions.final
class MsgEditSudoersResponse(google.protobuf.message.Message):
    """MsgEditSudoersResponse indicates the successful execution of MsgEditSudeors."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___MsgEditSudoersResponse = MsgEditSudoersResponse

@typing_extensions.final
class MsgChangeRoot(google.protobuf.message.Message):
    """-------------------------- ChangeRoot --------------------------

    MsgChangeRoot: Msg to update the "Sudoers" state.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SENDER_FIELD_NUMBER: builtins.int
    NEW_ROOT_FIELD_NUMBER: builtins.int
    sender: builtins.str
    """Sender: Address for the signer of the transaction."""
    new_root: builtins.str
    """NewRoot: New root address."""
    def __init__(
        self,
        *,
        sender: builtins.str = ...,
        new_root: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["new_root", b"new_root", "sender", b"sender"]) -> None: ...

global___MsgChangeRoot = MsgChangeRoot

@typing_extensions.final
class MsgChangeRootResponse(google.protobuf.message.Message):
    """MsgChangeRootResponse indicates the successful execution of MsgChangeRoot."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___MsgChangeRootResponse = MsgChangeRootResponse
