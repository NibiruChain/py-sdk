# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/tx/config/v1/config.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cosmos.app.v1alpha1 import module_pb2 as cosmos_dot_app_dot_v1alpha1_dot_module__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n cosmos/tx/config/v1/config.proto\x12\x13\x63osmos.tx.config.v1\x1a cosmos/app/v1alpha1/module.proto\"\x90\x01\n\x06\x43onfig\x12*\n\x11skip_ante_handler\x18\x01 \x01(\x08R\x0fskipAnteHandler\x12*\n\x11skip_post_handler\x18\x02 \x01(\x08R\x0fskipPostHandler:.\xba\xc0\x96\xda\x01(\n&github.com/cosmos/cosmos-sdk/x/auth/txb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.tx.config.v1.config_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CONFIG._options = None
  _CONFIG._serialized_options = b'\272\300\226\332\001(\n&github.com/cosmos/cosmos-sdk/x/auth/tx'
  _CONFIG._serialized_start=92
  _CONFIG._serialized_end=236
# @@protoc_insertion_point(module_scope)
