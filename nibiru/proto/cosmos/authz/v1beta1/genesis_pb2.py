# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/authz/v1beta1/genesis.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cosmos.authz.v1beta1 import (
    authz_pb2 as cosmos_dot_authz_dot_v1beta1_dot_authz__pb2,
)
from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\"cosmos/authz/v1beta1/genesis.proto\x12\x14\x63osmos.authz.v1beta1\x1a\x14gogoproto/gogo.proto\x1a cosmos/authz/v1beta1/authz.proto\"U\n\x0cGenesisState\x12\x45\n\rauthorization\x18\x01 \x03(\x0b\x32(.cosmos.authz.v1beta1.GrantAuthorizationB\x04\xc8\xde\x1f\x00\x42&Z$github.com/cosmos/cosmos-sdk/x/authzb\x06proto3'
)


_GENESISSTATE = DESCRIPTOR.message_types_by_name['GenesisState']
GenesisState = _reflection.GeneratedProtocolMessageType(
    'GenesisState',
    (_message.Message,),
    {
        'DESCRIPTOR': _GENESISSTATE,
        '__module__': 'cosmos.authz.v1beta1.genesis_pb2'
        # @@protoc_insertion_point(class_scope:cosmos.authz.v1beta1.GenesisState)
    },
)
_sym_db.RegisterMessage(GenesisState)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z$github.com/cosmos/cosmos-sdk/x/authz'
    _GENESISSTATE.fields_by_name['authorization']._options = None
    _GENESISSTATE.fields_by_name['authorization']._serialized_options = b'\310\336\037\000'
    _GENESISSTATE._serialized_start = 116
    _GENESISSTATE._serialized_end = 201
# @@protoc_insertion_point(module_scope)
