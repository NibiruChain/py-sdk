"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Since: cosmos-sdk 0.46"""
import builtins
import collections.abc
import google.protobuf.any_pb2
import google.protobuf.descriptor
import google.protobuf.duration_pb2
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _VoteOption:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _VoteOptionEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_VoteOption.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    VOTE_OPTION_UNSPECIFIED: _VoteOption.ValueType  # 0
    """VOTE_OPTION_UNSPECIFIED defines an unspecified vote option which will
    return an error.
    """
    VOTE_OPTION_YES: _VoteOption.ValueType  # 1
    """VOTE_OPTION_YES defines a yes vote option."""
    VOTE_OPTION_ABSTAIN: _VoteOption.ValueType  # 2
    """VOTE_OPTION_ABSTAIN defines an abstain vote option."""
    VOTE_OPTION_NO: _VoteOption.ValueType  # 3
    """VOTE_OPTION_NO defines a no vote option."""
    VOTE_OPTION_NO_WITH_VETO: _VoteOption.ValueType  # 4
    """VOTE_OPTION_NO_WITH_VETO defines a no with veto vote option."""

class VoteOption(_VoteOption, metaclass=_VoteOptionEnumTypeWrapper):
    """VoteOption enumerates the valid vote options for a given proposal."""

VOTE_OPTION_UNSPECIFIED: VoteOption.ValueType  # 0
"""VOTE_OPTION_UNSPECIFIED defines an unspecified vote option which will
return an error.
"""
VOTE_OPTION_YES: VoteOption.ValueType  # 1
"""VOTE_OPTION_YES defines a yes vote option."""
VOTE_OPTION_ABSTAIN: VoteOption.ValueType  # 2
"""VOTE_OPTION_ABSTAIN defines an abstain vote option."""
VOTE_OPTION_NO: VoteOption.ValueType  # 3
"""VOTE_OPTION_NO defines a no vote option."""
VOTE_OPTION_NO_WITH_VETO: VoteOption.ValueType  # 4
"""VOTE_OPTION_NO_WITH_VETO defines a no with veto vote option."""
global___VoteOption = VoteOption

class _ProposalStatus:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _ProposalStatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ProposalStatus.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PROPOSAL_STATUS_UNSPECIFIED: _ProposalStatus.ValueType  # 0
    """An empty value is invalid and not allowed."""
    PROPOSAL_STATUS_SUBMITTED: _ProposalStatus.ValueType  # 1
    """Initial status of a proposal when submitted."""
    PROPOSAL_STATUS_ACCEPTED: _ProposalStatus.ValueType  # 2
    """Final status of a proposal when the final tally is done and the outcome
    passes the group policy's decision policy.
    """
    PROPOSAL_STATUS_REJECTED: _ProposalStatus.ValueType  # 3
    """Final status of a proposal when the final tally is done and the outcome
    is rejected by the group policy's decision policy.
    """
    PROPOSAL_STATUS_ABORTED: _ProposalStatus.ValueType  # 4
    """Final status of a proposal when the group policy is modified before the
    final tally.
    """
    PROPOSAL_STATUS_WITHDRAWN: _ProposalStatus.ValueType  # 5
    """A proposal can be withdrawn before the voting start time by the owner.
    When this happens the final status is Withdrawn.
    """

class ProposalStatus(_ProposalStatus, metaclass=_ProposalStatusEnumTypeWrapper):
    """ProposalStatus defines proposal statuses."""

PROPOSAL_STATUS_UNSPECIFIED: ProposalStatus.ValueType  # 0
"""An empty value is invalid and not allowed."""
PROPOSAL_STATUS_SUBMITTED: ProposalStatus.ValueType  # 1
"""Initial status of a proposal when submitted."""
PROPOSAL_STATUS_ACCEPTED: ProposalStatus.ValueType  # 2
"""Final status of a proposal when the final tally is done and the outcome
passes the group policy's decision policy.
"""
PROPOSAL_STATUS_REJECTED: ProposalStatus.ValueType  # 3
"""Final status of a proposal when the final tally is done and the outcome
is rejected by the group policy's decision policy.
"""
PROPOSAL_STATUS_ABORTED: ProposalStatus.ValueType  # 4
"""Final status of a proposal when the group policy is modified before the
final tally.
"""
PROPOSAL_STATUS_WITHDRAWN: ProposalStatus.ValueType  # 5
"""A proposal can be withdrawn before the voting start time by the owner.
When this happens the final status is Withdrawn.
"""
global___ProposalStatus = ProposalStatus

class _ProposalExecutorResult:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _ProposalExecutorResultEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ProposalExecutorResult.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PROPOSAL_EXECUTOR_RESULT_UNSPECIFIED: _ProposalExecutorResult.ValueType  # 0
    """An empty value is not allowed."""
    PROPOSAL_EXECUTOR_RESULT_NOT_RUN: _ProposalExecutorResult.ValueType  # 1
    """We have not yet run the executor."""
    PROPOSAL_EXECUTOR_RESULT_SUCCESS: _ProposalExecutorResult.ValueType  # 2
    """The executor was successful and proposed action updated state."""
    PROPOSAL_EXECUTOR_RESULT_FAILURE: _ProposalExecutorResult.ValueType  # 3
    """The executor returned an error and proposed action didn't update state."""

class ProposalExecutorResult(_ProposalExecutorResult, metaclass=_ProposalExecutorResultEnumTypeWrapper):
    """ProposalExecutorResult defines types of proposal executor results."""

PROPOSAL_EXECUTOR_RESULT_UNSPECIFIED: ProposalExecutorResult.ValueType  # 0
"""An empty value is not allowed."""
PROPOSAL_EXECUTOR_RESULT_NOT_RUN: ProposalExecutorResult.ValueType  # 1
"""We have not yet run the executor."""
PROPOSAL_EXECUTOR_RESULT_SUCCESS: ProposalExecutorResult.ValueType  # 2
"""The executor was successful and proposed action updated state."""
PROPOSAL_EXECUTOR_RESULT_FAILURE: ProposalExecutorResult.ValueType  # 3
"""The executor returned an error and proposed action didn't update state."""
global___ProposalExecutorResult = ProposalExecutorResult

@typing_extensions.final
class Member(google.protobuf.message.Message):
    """Member represents a group member with an account address,
    non-zero weight, metadata and added_at timestamp.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ADDRESS_FIELD_NUMBER: builtins.int
    WEIGHT_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    ADDED_AT_FIELD_NUMBER: builtins.int
    address: builtins.str
    """address is the member's account address."""
    weight: builtins.str
    """weight is the member's voting weight that should be greater than 0."""
    metadata: builtins.str
    """metadata is any arbitrary metadata attached to the member."""
    @property
    def added_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """added_at is a timestamp specifying when a member was added."""
    def __init__(
        self,
        *,
        address: builtins.str = ...,
        weight: builtins.str = ...,
        metadata: builtins.str = ...,
        added_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["added_at", b"added_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["added_at", b"added_at", "address", b"address", "metadata", b"metadata", "weight", b"weight"]) -> None: ...

global___Member = Member

@typing_extensions.final
class MemberRequest(google.protobuf.message.Message):
    """MemberRequest represents a group member to be used in Msg server requests.
    Contrary to `Member`, it doesn't have any `added_at` field
    since this field cannot be set as part of requests.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ADDRESS_FIELD_NUMBER: builtins.int
    WEIGHT_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    address: builtins.str
    """address is the member's account address."""
    weight: builtins.str
    """weight is the member's voting weight that should be greater than 0."""
    metadata: builtins.str
    """metadata is any arbitrary metadata attached to the member."""
    def __init__(
        self,
        *,
        address: builtins.str = ...,
        weight: builtins.str = ...,
        metadata: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["address", b"address", "metadata", b"metadata", "weight", b"weight"]) -> None: ...

global___MemberRequest = MemberRequest

@typing_extensions.final
class ThresholdDecisionPolicy(google.protobuf.message.Message):
    """ThresholdDecisionPolicy is a decision policy where a proposal passes when it
    satisfies the two following conditions:
    1. The sum of all `YES` voter's weights is greater or equal than the defined
       `threshold`.
    2. The voting and execution periods of the proposal respect the parameters
       given by `windows`.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    THRESHOLD_FIELD_NUMBER: builtins.int
    WINDOWS_FIELD_NUMBER: builtins.int
    threshold: builtins.str
    """threshold is the minimum weighted sum of `YES` votes that must be met or
    exceeded for a proposal to succeed.
    """
    @property
    def windows(self) -> global___DecisionPolicyWindows:
        """windows defines the different windows for voting and execution."""
    def __init__(
        self,
        *,
        threshold: builtins.str = ...,
        windows: global___DecisionPolicyWindows | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["windows", b"windows"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["threshold", b"threshold", "windows", b"windows"]) -> None: ...

global___ThresholdDecisionPolicy = ThresholdDecisionPolicy

@typing_extensions.final
class PercentageDecisionPolicy(google.protobuf.message.Message):
    """PercentageDecisionPolicy is a decision policy where a proposal passes when
    it satisfies the two following conditions:
    1. The percentage of all `YES` voters' weights out of the total group weight
       is greater or equal than the given `percentage`.
    2. The voting and execution periods of the proposal respect the parameters
       given by `windows`.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PERCENTAGE_FIELD_NUMBER: builtins.int
    WINDOWS_FIELD_NUMBER: builtins.int
    percentage: builtins.str
    """percentage is the minimum percentage of the weighted sum of `YES` votes must
    meet for a proposal to succeed.
    """
    @property
    def windows(self) -> global___DecisionPolicyWindows:
        """windows defines the different windows for voting and execution."""
    def __init__(
        self,
        *,
        percentage: builtins.str = ...,
        windows: global___DecisionPolicyWindows | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["windows", b"windows"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["percentage", b"percentage", "windows", b"windows"]) -> None: ...

global___PercentageDecisionPolicy = PercentageDecisionPolicy

@typing_extensions.final
class DecisionPolicyWindows(google.protobuf.message.Message):
    """DecisionPolicyWindows defines the different windows for voting and execution."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VOTING_PERIOD_FIELD_NUMBER: builtins.int
    MIN_EXECUTION_PERIOD_FIELD_NUMBER: builtins.int
    @property
    def voting_period(self) -> google.protobuf.duration_pb2.Duration:
        """voting_period is the duration from submission of a proposal to the end of voting period
        Within this times votes can be submitted with MsgVote.
        """
    @property
    def min_execution_period(self) -> google.protobuf.duration_pb2.Duration:
        """min_execution_period is the minimum duration after the proposal submission
        where members can start sending MsgExec. This means that the window for
        sending a MsgExec transaction is:
        `[ submission + min_execution_period ; submission + voting_period + max_execution_period]`
        where max_execution_period is a app-specific config, defined in the keeper.
        If not set, min_execution_period will default to 0.

        Please make sure to set a `min_execution_period` that is smaller than
        `voting_period + max_execution_period`, or else the above execution window
        is empty, meaning that all proposals created with this decision policy
        won't be able to be executed.
        """
    def __init__(
        self,
        *,
        voting_period: google.protobuf.duration_pb2.Duration | None = ...,
        min_execution_period: google.protobuf.duration_pb2.Duration | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["min_execution_period", b"min_execution_period", "voting_period", b"voting_period"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["min_execution_period", b"min_execution_period", "voting_period", b"voting_period"]) -> None: ...

global___DecisionPolicyWindows = DecisionPolicyWindows

@typing_extensions.final
class GroupInfo(google.protobuf.message.Message):
    """
    State

    GroupInfo represents the high-level on-chain information for a group.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    ADMIN_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    VERSION_FIELD_NUMBER: builtins.int
    TOTAL_WEIGHT_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    id: builtins.int
    """id is the unique ID of the group."""
    admin: builtins.str
    """admin is the account address of the group's admin."""
    metadata: builtins.str
    """metadata is any arbitrary metadata to attached to the group."""
    version: builtins.int
    """version is used to track changes to a group's membership structure that
    would break existing proposals. Whenever any members weight is changed,
    or any member is added or removed this version is incremented and will
    cause proposals based on older versions of this group to fail
    """
    total_weight: builtins.str
    """total_weight is the sum of the group members' weights."""
    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """created_at is a timestamp specifying when a group was created."""
    def __init__(
        self,
        *,
        id: builtins.int = ...,
        admin: builtins.str = ...,
        metadata: builtins.str = ...,
        version: builtins.int = ...,
        total_weight: builtins.str = ...,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["created_at", b"created_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["admin", b"admin", "created_at", b"created_at", "id", b"id", "metadata", b"metadata", "total_weight", b"total_weight", "version", b"version"]) -> None: ...

global___GroupInfo = GroupInfo

@typing_extensions.final
class GroupMember(google.protobuf.message.Message):
    """GroupMember represents the relationship between a group and a member."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    GROUP_ID_FIELD_NUMBER: builtins.int
    MEMBER_FIELD_NUMBER: builtins.int
    group_id: builtins.int
    """group_id is the unique ID of the group."""
    @property
    def member(self) -> global___Member:
        """member is the member data."""
    def __init__(
        self,
        *,
        group_id: builtins.int = ...,
        member: global___Member | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["member", b"member"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["group_id", b"group_id", "member", b"member"]) -> None: ...

global___GroupMember = GroupMember

@typing_extensions.final
class GroupPolicyInfo(google.protobuf.message.Message):
    """GroupPolicyInfo represents the high-level on-chain information for a group policy."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ADDRESS_FIELD_NUMBER: builtins.int
    GROUP_ID_FIELD_NUMBER: builtins.int
    ADMIN_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    VERSION_FIELD_NUMBER: builtins.int
    DECISION_POLICY_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    address: builtins.str
    """address is the account address of group policy."""
    group_id: builtins.int
    """group_id is the unique ID of the group."""
    admin: builtins.str
    """admin is the account address of the group admin."""
    metadata: builtins.str
    """metadata is any arbitrary metadata attached to the group policy.
    the recommended format of the metadata is to be found here:
    https://docs.cosmos.network/v0.47/modules/group#decision-policy-1
    """
    version: builtins.int
    """version is used to track changes to a group's GroupPolicyInfo structure that
    would create a different result on a running proposal.
    """
    @property
    def decision_policy(self) -> google.protobuf.any_pb2.Any:
        """decision_policy specifies the group policy's decision policy."""
    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """created_at is a timestamp specifying when a group policy was created."""
    def __init__(
        self,
        *,
        address: builtins.str = ...,
        group_id: builtins.int = ...,
        admin: builtins.str = ...,
        metadata: builtins.str = ...,
        version: builtins.int = ...,
        decision_policy: google.protobuf.any_pb2.Any | None = ...,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["created_at", b"created_at", "decision_policy", b"decision_policy"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["address", b"address", "admin", b"admin", "created_at", b"created_at", "decision_policy", b"decision_policy", "group_id", b"group_id", "metadata", b"metadata", "version", b"version"]) -> None: ...

global___GroupPolicyInfo = GroupPolicyInfo

@typing_extensions.final
class Proposal(google.protobuf.message.Message):
    """Proposal defines a group proposal. Any member of a group can submit a proposal
    for a group policy to decide upon.
    A proposal consists of a set of `sdk.Msg`s that will be executed if the proposal
    passes as well as some optional metadata associated with the proposal.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    GROUP_POLICY_ADDRESS_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    PROPOSERS_FIELD_NUMBER: builtins.int
    SUBMIT_TIME_FIELD_NUMBER: builtins.int
    GROUP_VERSION_FIELD_NUMBER: builtins.int
    GROUP_POLICY_VERSION_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    FINAL_TALLY_RESULT_FIELD_NUMBER: builtins.int
    VOTING_PERIOD_END_FIELD_NUMBER: builtins.int
    EXECUTOR_RESULT_FIELD_NUMBER: builtins.int
    MESSAGES_FIELD_NUMBER: builtins.int
    TITLE_FIELD_NUMBER: builtins.int
    SUMMARY_FIELD_NUMBER: builtins.int
    id: builtins.int
    """id is the unique id of the proposal."""
    group_policy_address: builtins.str
    """group_policy_address is the account address of group policy."""
    metadata: builtins.str
    """metadata is any arbitrary metadata attached to the proposal.
    the recommended format of the metadata is to be found here:
    https://docs.cosmos.network/v0.47/modules/group#proposal-4
    """
    @property
    def proposers(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """proposers are the account addresses of the proposers."""
    @property
    def submit_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """submit_time is a timestamp specifying when a proposal was submitted."""
    group_version: builtins.int
    """group_version tracks the version of the group at proposal submission.
    This field is here for informational purposes only.
    """
    group_policy_version: builtins.int
    """group_policy_version tracks the version of the group policy at proposal submission.
    When a decision policy is changed, existing proposals from previous policy
    versions will become invalid with the `ABORTED` status.
    This field is here for informational purposes only.
    """
    status: global___ProposalStatus.ValueType
    """status represents the high level position in the life cycle of the proposal. Initial value is Submitted."""
    @property
    def final_tally_result(self) -> global___TallyResult:
        """final_tally_result contains the sums of all weighted votes for this
        proposal for each vote option. It is empty at submission, and only
        populated after tallying, at voting period end or at proposal execution,
        whichever happens first.
        """
    @property
    def voting_period_end(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """voting_period_end is the timestamp before which voting must be done.
        Unless a successful MsgExec is called before (to execute a proposal whose
        tally is successful before the voting period ends), tallying will be done
        at this point, and the `final_tally_result`and `status` fields will be
        accordingly updated.
        """
    executor_result: global___ProposalExecutorResult.ValueType
    """executor_result is the final result of the proposal execution. Initial value is NotRun."""
    @property
    def messages(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[google.protobuf.any_pb2.Any]:
        """messages is a list of `sdk.Msg`s that will be executed if the proposal passes."""
    title: builtins.str
    """title is the title of the proposal

    Since: cosmos-sdk 0.47
    """
    summary: builtins.str
    """summary is a short summary of the proposal

    Since: cosmos-sdk 0.47
    """
    def __init__(
        self,
        *,
        id: builtins.int = ...,
        group_policy_address: builtins.str = ...,
        metadata: builtins.str = ...,
        proposers: collections.abc.Iterable[builtins.str] | None = ...,
        submit_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        group_version: builtins.int = ...,
        group_policy_version: builtins.int = ...,
        status: global___ProposalStatus.ValueType = ...,
        final_tally_result: global___TallyResult | None = ...,
        voting_period_end: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        executor_result: global___ProposalExecutorResult.ValueType = ...,
        messages: collections.abc.Iterable[google.protobuf.any_pb2.Any] | None = ...,
        title: builtins.str = ...,
        summary: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["final_tally_result", b"final_tally_result", "submit_time", b"submit_time", "voting_period_end", b"voting_period_end"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["executor_result", b"executor_result", "final_tally_result", b"final_tally_result", "group_policy_address", b"group_policy_address", "group_policy_version", b"group_policy_version", "group_version", b"group_version", "id", b"id", "messages", b"messages", "metadata", b"metadata", "proposers", b"proposers", "status", b"status", "submit_time", b"submit_time", "summary", b"summary", "title", b"title", "voting_period_end", b"voting_period_end"]) -> None: ...

global___Proposal = Proposal

@typing_extensions.final
class TallyResult(google.protobuf.message.Message):
    """TallyResult represents the sum of weighted votes for each vote option."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    YES_COUNT_FIELD_NUMBER: builtins.int
    ABSTAIN_COUNT_FIELD_NUMBER: builtins.int
    NO_COUNT_FIELD_NUMBER: builtins.int
    NO_WITH_VETO_COUNT_FIELD_NUMBER: builtins.int
    yes_count: builtins.str
    """yes_count is the weighted sum of yes votes."""
    abstain_count: builtins.str
    """abstain_count is the weighted sum of abstainers."""
    no_count: builtins.str
    """no_count is the weighted sum of no votes."""
    no_with_veto_count: builtins.str
    """no_with_veto_count is the weighted sum of veto."""
    def __init__(
        self,
        *,
        yes_count: builtins.str = ...,
        abstain_count: builtins.str = ...,
        no_count: builtins.str = ...,
        no_with_veto_count: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["abstain_count", b"abstain_count", "no_count", b"no_count", "no_with_veto_count", b"no_with_veto_count", "yes_count", b"yes_count"]) -> None: ...

global___TallyResult = TallyResult

@typing_extensions.final
class Vote(google.protobuf.message.Message):
    """Vote represents a vote for a proposal."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PROPOSAL_ID_FIELD_NUMBER: builtins.int
    VOTER_FIELD_NUMBER: builtins.int
    OPTION_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    SUBMIT_TIME_FIELD_NUMBER: builtins.int
    proposal_id: builtins.int
    """proposal is the unique ID of the proposal."""
    voter: builtins.str
    """voter is the account address of the voter."""
    option: global___VoteOption.ValueType
    """option is the voter's choice on the proposal."""
    metadata: builtins.str
    """metadata is any arbitrary metadata attached to the vote."""
    @property
    def submit_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """submit_time is the timestamp when the vote was submitted."""
    def __init__(
        self,
        *,
        proposal_id: builtins.int = ...,
        voter: builtins.str = ...,
        option: global___VoteOption.ValueType = ...,
        metadata: builtins.str = ...,
        submit_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["submit_time", b"submit_time"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["metadata", b"metadata", "option", b"option", "proposal_id", b"proposal_id", "submit_time", b"submit_time", "voter", b"voter"]) -> None: ...

global___Vote = Vote