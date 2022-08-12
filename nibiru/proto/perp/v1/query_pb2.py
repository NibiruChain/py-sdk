# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: perp/v1/query.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from perp.v1 import state_pb2 as perp_dot_v1_dot_state__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x13perp/v1/query.proto\x12\x0enibiru.perp.v1\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x13perp/v1/state.proto\"\x14\n\x12QueryParamsRequest\"C\n\x13QueryParamsResponse\x12,\n\x06params\x18\x01 \x01(\x0b\x32\x16.nibiru.perp.v1.ParamsB\x04\xc8\xde\x1f\x00\"@\n\x1aQueryTraderPositionRequest\x12\x12\n\ntoken_pair\x18\x01 \x01(\t\x12\x0e\n\x06trader\x18\x02 \x01(\t\"\x89\x03\n\x1bQueryTraderPositionResponse\x12*\n\x08position\x18\x01 \x01(\x0b\x32\x18.nibiru.perp.v1.Position\x12I\n\x11position_notional\x18\x02 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12\x46\n\x0eunrealized_pnl\x18\x03 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12I\n\x11margin_ratio_mark\x18\x04 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12J\n\x12margin_ratio_index\x18\x05 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12\x14\n\x0c\x62lock_number\x18\x07 \x01(\x03\x32\x8e\x02\n\x05Query\x12n\n\x06Params\x12\".nibiru.perp.v1.QueryParamsRequest\x1a#.nibiru.perp.v1.QueryParamsResponse\"\x1b\x82\xd3\xe4\x93\x02\x15\x12\x13/nibiru/perp/params\x12\x94\x01\n\x13QueryTraderPosition\x12*.nibiru.perp.v1.QueryTraderPositionRequest\x1a+.nibiru.perp.v1.QueryTraderPositionResponse\"$\x82\xd3\xe4\x93\x02\x1e\x12\x1c/nibiru/perp/trader_positionB,Z*github.com/NibiruChain/nibiru/x/perp/typesb\x06proto3'
)


_QUERYPARAMSREQUEST = DESCRIPTOR.message_types_by_name['QueryParamsRequest']
_QUERYPARAMSRESPONSE = DESCRIPTOR.message_types_by_name['QueryParamsResponse']
_QUERYTRADERPOSITIONREQUEST = DESCRIPTOR.message_types_by_name['QueryTraderPositionRequest']
_QUERYTRADERPOSITIONRESPONSE = DESCRIPTOR.message_types_by_name['QueryTraderPositionResponse']
QueryParamsRequest = _reflection.GeneratedProtocolMessageType(
    'QueryParamsRequest',
    (_message.Message,),
    {
        'DESCRIPTOR': _QUERYPARAMSREQUEST,
        '__module__': 'perp.v1.query_pb2'
        # @@protoc_insertion_point(class_scope:nibiru.perp.v1.QueryParamsRequest)
    },
)
_sym_db.RegisterMessage(QueryParamsRequest)

QueryParamsResponse = _reflection.GeneratedProtocolMessageType(
    'QueryParamsResponse',
    (_message.Message,),
    {
        'DESCRIPTOR': _QUERYPARAMSRESPONSE,
        '__module__': 'perp.v1.query_pb2'
        # @@protoc_insertion_point(class_scope:nibiru.perp.v1.QueryParamsResponse)
    },
)
_sym_db.RegisterMessage(QueryParamsResponse)

QueryTraderPositionRequest = _reflection.GeneratedProtocolMessageType(
    'QueryTraderPositionRequest',
    (_message.Message,),
    {
        'DESCRIPTOR': _QUERYTRADERPOSITIONREQUEST,
        '__module__': 'perp.v1.query_pb2'
        # @@protoc_insertion_point(class_scope:nibiru.perp.v1.QueryTraderPositionRequest)
    },
)
_sym_db.RegisterMessage(QueryTraderPositionRequest)

QueryTraderPositionResponse = _reflection.GeneratedProtocolMessageType(
    'QueryTraderPositionResponse',
    (_message.Message,),
    {
        'DESCRIPTOR': _QUERYTRADERPOSITIONRESPONSE,
        '__module__': 'perp.v1.query_pb2'
        # @@protoc_insertion_point(class_scope:nibiru.perp.v1.QueryTraderPositionResponse)
    },
)
_sym_db.RegisterMessage(QueryTraderPositionResponse)

_QUERY = DESCRIPTOR.services_by_name['Query']
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z*github.com/NibiruChain/nibiru/x/perp/types'
    _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
    _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\310\336\037\000'
    _QUERYTRADERPOSITIONRESPONSE.fields_by_name['position_notional']._options = None
    _QUERYTRADERPOSITIONRESPONSE.fields_by_name[
        'position_notional'
    ]._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
    _QUERYTRADERPOSITIONRESPONSE.fields_by_name['unrealized_pnl']._options = None
    _QUERYTRADERPOSITIONRESPONSE.fields_by_name[
        'unrealized_pnl'
    ]._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
    _QUERYTRADERPOSITIONRESPONSE.fields_by_name['margin_ratio_mark']._options = None
    _QUERYTRADERPOSITIONRESPONSE.fields_by_name[
        'margin_ratio_mark'
    ]._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
    _QUERYTRADERPOSITIONRESPONSE.fields_by_name['margin_ratio_index']._options = None
    _QUERYTRADERPOSITIONRESPONSE.fields_by_name[
        'margin_ratio_index'
    ]._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
    _QUERY.methods_by_name['Params']._options = None
    _QUERY.methods_by_name['Params']._serialized_options = b'\202\323\344\223\002\025\022\023/nibiru/perp/params'
    _QUERY.methods_by_name['QueryTraderPosition']._options = None
    _QUERY.methods_by_name[
        'QueryTraderPosition'
    ]._serialized_options = b'\202\323\344\223\002\036\022\034/nibiru/perp/trader_position'
    _QUERYPARAMSREQUEST._serialized_start = 112
    _QUERYPARAMSREQUEST._serialized_end = 132
    _QUERYPARAMSRESPONSE._serialized_start = 134
    _QUERYPARAMSRESPONSE._serialized_end = 201
    _QUERYTRADERPOSITIONREQUEST._serialized_start = 203
    _QUERYTRADERPOSITIONREQUEST._serialized_end = 267
    _QUERYTRADERPOSITIONRESPONSE._serialized_start = 270
    _QUERYTRADERPOSITIONRESPONSE._serialized_end = 663
    _QUERY._serialized_start = 666
    _QUERY._serialized_end = 936
# @@protoc_insertion_point(module_scope)
