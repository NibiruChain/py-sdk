"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import cosmos.base.abci.v1beta1.abci_pb2
import cosmos.base.query.v1beta1.pagination_pb2
import cosmos.tx.v1beta1.tx_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import tendermint.types.block_pb2
import tendermint.types.types_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _OrderBy:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _OrderByEnumTypeWrapper(
    google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_OrderBy.ValueType], builtins.type
):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    ORDER_BY_UNSPECIFIED: _OrderBy.ValueType  # 0
    """ORDER_BY_UNSPECIFIED specifies an unknown sorting order. OrderBy defaults to ASC in this case."""

    ORDER_BY_ASC: _OrderBy.ValueType  # 1
    """ORDER_BY_ASC defines ascending order"""

    ORDER_BY_DESC: _OrderBy.ValueType  # 2
    """ORDER_BY_DESC defines descending order"""

class OrderBy(_OrderBy, metaclass=_OrderByEnumTypeWrapper):
    """OrderBy defines the sorting order"""

    pass

ORDER_BY_UNSPECIFIED: OrderBy.ValueType  # 0
"""ORDER_BY_UNSPECIFIED specifies an unknown sorting order. OrderBy defaults to ASC in this case."""

ORDER_BY_ASC: OrderBy.ValueType  # 1
"""ORDER_BY_ASC defines ascending order"""

ORDER_BY_DESC: OrderBy.ValueType  # 2
"""ORDER_BY_DESC defines descending order"""

global___OrderBy = OrderBy

class _BroadcastMode:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _BroadcastModeEnumTypeWrapper(
    google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_BroadcastMode.ValueType], builtins.type
):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    BROADCAST_MODE_UNSPECIFIED: _BroadcastMode.ValueType  # 0
    """zero-value for mode ordering"""

    BROADCAST_MODE_BLOCK: _BroadcastMode.ValueType  # 1
    """BROADCAST_MODE_BLOCK defines a tx broadcasting mode where the client waits for
    the tx to be committed in a block.
    """

    BROADCAST_MODE_SYNC: _BroadcastMode.ValueType  # 2
    """BROADCAST_MODE_SYNC defines a tx broadcasting mode where the client waits for
    a CheckTx execution response only.
    """

    BROADCAST_MODE_ASYNC: _BroadcastMode.ValueType  # 3
    """BROADCAST_MODE_defines a tx broadcasting mode where the client returns
    immediately.
    """

class BroadcastMode(_BroadcastMode, metaclass=_BroadcastModeEnumTypeWrapper):
    """BroadcastMode specifies the broadcast mode for the TxService.Broadcast RPC method."""

    pass

BROADCAST_MODE_UNSPECIFIED: BroadcastMode.ValueType  # 0
"""zero-value for mode ordering"""

BROADCAST_MODE_BLOCK: BroadcastMode.ValueType  # 1
"""BROADCAST_MODE_BLOCK defines a tx broadcasting mode where the client waits for
the tx to be committed in a block.
"""

BROADCAST_MODE_SYNC: BroadcastMode.ValueType  # 2
"""BROADCAST_MODE_SYNC defines a tx broadcasting mode where the client waits for
a CheckTx execution response only.
"""

BROADCAST_MODE_ASYNC: BroadcastMode.ValueType  # 3
"""BROADCAST_MODE_defines a tx broadcasting mode where the client returns
immediately.
"""

global___BroadcastMode = BroadcastMode

class GetTxsEventRequest(google.protobuf.message.Message):
    """GetTxsEventRequest is the request type for the Service.TxsByEvents
    RPC method.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    EVENTS_FIELD_NUMBER: builtins.int
    PAGINATION_FIELD_NUMBER: builtins.int
    ORDER_BY_FIELD_NUMBER: builtins.int
    @property
    def events(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """events is the list of transaction event type."""
        pass
    @property
    def pagination(self) -> cosmos.base.query.v1beta1.pagination_pb2.PageRequest:
        """pagination defines a pagination for the request."""
        pass
    order_by: global___OrderBy.ValueType
    def __init__(
        self,
        *,
        events: typing.Optional[typing.Iterable[typing.Text]] = ...,
        pagination: typing.Optional[cosmos.base.query.v1beta1.pagination_pb2.PageRequest] = ...,
        order_by: global___OrderBy.ValueType = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["pagination", b"pagination"]) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "events", b"events", "order_by", b"order_by", "pagination", b"pagination"
        ],
    ) -> None: ...

global___GetTxsEventRequest = GetTxsEventRequest

class GetTxsEventResponse(google.protobuf.message.Message):
    """GetTxsEventResponse is the response type for the Service.TxsByEvents
    RPC method.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TXS_FIELD_NUMBER: builtins.int
    TX_RESPONSES_FIELD_NUMBER: builtins.int
    PAGINATION_FIELD_NUMBER: builtins.int
    @property
    def txs(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[cosmos.tx.v1beta1.tx_pb2.Tx]:
        """txs is the list of queried transactions."""
        pass
    @property
    def tx_responses(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        cosmos.base.abci.v1beta1.abci_pb2.TxResponse
    ]:
        """tx_responses is the list of queried TxResponses."""
        pass
    @property
    def pagination(self) -> cosmos.base.query.v1beta1.pagination_pb2.PageResponse:
        """pagination defines a pagination for the response."""
        pass
    def __init__(
        self,
        *,
        txs: typing.Optional[typing.Iterable[cosmos.tx.v1beta1.tx_pb2.Tx]] = ...,
        tx_responses: typing.Optional[typing.Iterable[cosmos.base.abci.v1beta1.abci_pb2.TxResponse]] = ...,
        pagination: typing.Optional[cosmos.base.query.v1beta1.pagination_pb2.PageResponse] = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["pagination", b"pagination"]) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "pagination", b"pagination", "tx_responses", b"tx_responses", "txs", b"txs"
        ],
    ) -> None: ...

global___GetTxsEventResponse = GetTxsEventResponse

class BroadcastTxRequest(google.protobuf.message.Message):
    """BroadcastTxRequest is the request type for the Service.BroadcastTxRequest
    RPC method.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TX_BYTES_FIELD_NUMBER: builtins.int
    MODE_FIELD_NUMBER: builtins.int
    tx_bytes: builtins.bytes
    """tx_bytes is the raw transaction."""

    mode: global___BroadcastMode.ValueType
    def __init__(
        self,
        *,
        tx_bytes: builtins.bytes = ...,
        mode: global___BroadcastMode.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["mode", b"mode", "tx_bytes", b"tx_bytes"]) -> None: ...

global___BroadcastTxRequest = BroadcastTxRequest

class BroadcastTxResponse(google.protobuf.message.Message):
    """BroadcastTxResponse is the response type for the
    Service.BroadcastTx method.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TX_RESPONSE_FIELD_NUMBER: builtins.int
    @property
    def tx_response(self) -> cosmos.base.abci.v1beta1.abci_pb2.TxResponse:
        """tx_response is the queried TxResponses."""
        pass
    def __init__(
        self,
        *,
        tx_response: typing.Optional[cosmos.base.abci.v1beta1.abci_pb2.TxResponse] = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["tx_response", b"tx_response"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["tx_response", b"tx_response"]) -> None: ...

global___BroadcastTxResponse = BroadcastTxResponse

class SimulateRequest(google.protobuf.message.Message):
    """SimulateRequest is the request type for the Service.Simulate
    RPC method.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TX_FIELD_NUMBER: builtins.int
    TX_BYTES_FIELD_NUMBER: builtins.int
    @property
    def tx(self) -> cosmos.tx.v1beta1.tx_pb2.Tx:
        """tx is the transaction to simulate.
        Deprecated. Send raw tx bytes instead.
        """
        pass
    tx_bytes: builtins.bytes
    """tx_bytes is the raw transaction.

    Since: cosmos-sdk 0.43
    """
    def __init__(
        self,
        *,
        tx: typing.Optional[cosmos.tx.v1beta1.tx_pb2.Tx] = ...,
        tx_bytes: builtins.bytes = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["tx", b"tx"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["tx", b"tx", "tx_bytes", b"tx_bytes"]) -> None: ...

global___SimulateRequest = SimulateRequest

class SimulateResponse(google.protobuf.message.Message):
    """SimulateResponse is the response type for the
    Service.SimulateRPC method.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    GAS_INFO_FIELD_NUMBER: builtins.int
    RESULT_FIELD_NUMBER: builtins.int
    @property
    def gas_info(self) -> cosmos.base.abci.v1beta1.abci_pb2.GasInfo:
        """gas_info is the information about gas used in the simulation."""
        pass
    @property
    def result(self) -> cosmos.base.abci.v1beta1.abci_pb2.Result:
        """result is the result of the simulation."""
        pass
    def __init__(
        self,
        *,
        gas_info: typing.Optional[cosmos.base.abci.v1beta1.abci_pb2.GasInfo] = ...,
        result: typing.Optional[cosmos.base.abci.v1beta1.abci_pb2.Result] = ...,
    ) -> None: ...
    def HasField(
        self, field_name: typing_extensions.Literal["gas_info", b"gas_info", "result", b"result"]
    ) -> builtins.bool: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["gas_info", b"gas_info", "result", b"result"]
    ) -> None: ...

global___SimulateResponse = SimulateResponse

class GetTxRequest(google.protobuf.message.Message):
    """GetTxRequest is the request type for the Service.GetTx
    RPC method.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    HASH_FIELD_NUMBER: builtins.int
    hash: typing.Text
    """hash is the tx hash to query, encoded as a hex string."""
    def __init__(
        self,
        *,
        hash: typing.Text = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["hash", b"hash"]) -> None: ...

global___GetTxRequest = GetTxRequest

class GetTxResponse(google.protobuf.message.Message):
    """GetTxResponse is the response type for the Service.GetTx method."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TX_FIELD_NUMBER: builtins.int
    TX_RESPONSE_FIELD_NUMBER: builtins.int
    @property
    def tx(self) -> cosmos.tx.v1beta1.tx_pb2.Tx:
        """tx is the queried transaction."""
        pass
    @property
    def tx_response(self) -> cosmos.base.abci.v1beta1.abci_pb2.TxResponse:
        """tx_response is the queried TxResponses."""
        pass
    def __init__(
        self,
        *,
        tx: typing.Optional[cosmos.tx.v1beta1.tx_pb2.Tx] = ...,
        tx_response: typing.Optional[cosmos.base.abci.v1beta1.abci_pb2.TxResponse] = ...,
    ) -> None: ...
    def HasField(
        self, field_name: typing_extensions.Literal["tx", b"tx", "tx_response", b"tx_response"]
    ) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["tx", b"tx", "tx_response", b"tx_response"]) -> None: ...

global___GetTxResponse = GetTxResponse

class GetBlockWithTxsRequest(google.protobuf.message.Message):
    """GetBlockWithTxsRequest is the request type for the Service.GetBlockWithTxs
    RPC method.

    Since: cosmos-sdk 0.45.2
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    HEIGHT_FIELD_NUMBER: builtins.int
    PAGINATION_FIELD_NUMBER: builtins.int
    height: builtins.int
    """height is the height of the block to query."""
    @property
    def pagination(self) -> cosmos.base.query.v1beta1.pagination_pb2.PageRequest:
        """pagination defines a pagination for the request."""
        pass
    def __init__(
        self,
        *,
        height: builtins.int = ...,
        pagination: typing.Optional[cosmos.base.query.v1beta1.pagination_pb2.PageRequest] = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["pagination", b"pagination"]) -> builtins.bool: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["height", b"height", "pagination", b"pagination"]
    ) -> None: ...

global___GetBlockWithTxsRequest = GetBlockWithTxsRequest

class GetBlockWithTxsResponse(google.protobuf.message.Message):
    """GetBlockWithTxsResponse is the response type for the Service.GetBlockWithTxs method.

    Since: cosmos-sdk 0.45.2
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TXS_FIELD_NUMBER: builtins.int
    BLOCK_ID_FIELD_NUMBER: builtins.int
    BLOCK_FIELD_NUMBER: builtins.int
    PAGINATION_FIELD_NUMBER: builtins.int
    @property
    def txs(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[cosmos.tx.v1beta1.tx_pb2.Tx]:
        """txs are the transactions in the block."""
        pass
    @property
    def block_id(self) -> tendermint.types.types_pb2.BlockID: ...
    @property
    def block(self) -> tendermint.types.block_pb2.Block: ...
    @property
    def pagination(self) -> cosmos.base.query.v1beta1.pagination_pb2.PageResponse:
        """pagination defines a pagination for the response."""
        pass
    def __init__(
        self,
        *,
        txs: typing.Optional[typing.Iterable[cosmos.tx.v1beta1.tx_pb2.Tx]] = ...,
        block_id: typing.Optional[tendermint.types.types_pb2.BlockID] = ...,
        block: typing.Optional[tendermint.types.block_pb2.Block] = ...,
        pagination: typing.Optional[cosmos.base.query.v1beta1.pagination_pb2.PageResponse] = ...,
    ) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions.Literal["block", b"block", "block_id", b"block_id", "pagination", b"pagination"],
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "block", b"block", "block_id", b"block_id", "pagination", b"pagination", "txs", b"txs"
        ],
    ) -> None: ...

global___GetBlockWithTxsResponse = GetBlockWithTxsResponse
