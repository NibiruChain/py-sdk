# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nibiru/oracle/v1/state.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from nibiru_proto.nibiru.oracle.v1 import oracle_pb2 as nibiru_dot_oracle_dot_v1_dot_oracle__pb2
from cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cnibiru/oracle/v1/state.proto\x12\x10nibiru.oracle.v1\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1dnibiru/oracle/v1/oracle.proto\x1a\x1e\x63osmos/base/v1beta1/coin.proto\"\xd6\x01\n\rPriceSnapshot\x12\\\n\x04pair\x18\x01 \x01(\tBH\xc8\xde\x1f\x00\xda\xde\x1f\x31github.com/NibiruChain/nibiru/x/common/asset.Pair\xf2\xde\x1f\x0byaml:\"pair\"R\x04pair\x12\x44\n\x05price\x18\x02 \x01(\tB.\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.DecR\x05price\x12!\n\x0ctimestamp_ms\x18\x03 \x01(\x03R\x0btimestampMsB.Z,github.com/NibiruChain/nibiru/x/oracle/typesb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nibiru.oracle.v1.state_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z,github.com/NibiruChain/nibiru/x/oracle/types'
  _PRICESNAPSHOT.fields_by_name['pair']._options = None
  _PRICESNAPSHOT.fields_by_name['pair']._serialized_options = b'\310\336\037\000\332\336\0371github.com/NibiruChain/nibiru/x/common/asset.Pair\362\336\037\013yaml:\"pair\"'
  _PRICESNAPSHOT.fields_by_name['price']._options = None
  _PRICESNAPSHOT.fields_by_name['price']._serialized_options = b'\310\336\037\000\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec'
  _PRICESNAPSHOT._serialized_start=166
  _PRICESNAPSHOT._serialized_end=380
# @@protoc_insertion_point(module_scope)