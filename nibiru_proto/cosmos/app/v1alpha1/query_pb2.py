# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/app/v1alpha1/query.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cosmos.app.v1alpha1 import config_pb2 as cosmos_dot_app_dot_v1alpha1_dot_config__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1f\x63osmos/app/v1alpha1/query.proto\x12\x13\x63osmos.app.v1alpha1\x1a cosmos/app/v1alpha1/config.proto\"\x14\n\x12QueryConfigRequest\"J\n\x13QueryConfigResponse\x12\x33\n\x06\x63onfig\x18\x01 \x01(\x0b\x32\x1b.cosmos.app.v1alpha1.ConfigR\x06\x63onfig2f\n\x05Query\x12]\n\x06\x43onfig\x12\'.cosmos.app.v1alpha1.QueryConfigRequest\x1a(.cosmos.app.v1alpha1.QueryConfigResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.app.v1alpha1.query_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _QUERYCONFIGREQUEST._serialized_start=90
  _QUERYCONFIGREQUEST._serialized_end=110
  _QUERYCONFIGRESPONSE._serialized_start=112
  _QUERYCONFIGRESPONSE._serialized_end=186
  _QUERY._serialized_start=188
  _QUERY._serialized_end=290
# @@protoc_insertion_point(module_scope)
