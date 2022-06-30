# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dex/v1/pool.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x64\x65x/v1/pool.proto\x12\rnibiru.dex.v1\x1a\x14gogoproto/gogo.proto\x1a\x1e\x63osmos/base/v1beta1/coin.proto\x1a\x19\x63osmos_proto/cosmos.proto\"\xb4\x01\n\nPoolParams\x12R\n\x07swapFee\x18\x01 \x01(\tBA\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x0fyaml:\"swap_fee\"\xc8\xde\x1f\x00\x12R\n\x07\x65xitFee\x18\x02 \x01(\tBA\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x0fyaml:\"exit_fee\"\xc8\xde\x1f\x00\"\x9c\x01\n\tPoolAsset\x12>\n\x05token\x18\x01 \x01(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x14\xf2\xde\x1f\x0cyaml:\"token\"\xc8\xde\x1f\x00\x12O\n\x06weight\x18\x02 \x01(\tB?\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\ryaml:\"weight\"\xc8\xde\x1f\x00\"\xfb\x02\n\x04Pool\x12\n\n\x02id\x18\x01 \x01(\x04\x12#\n\x07\x61\x64\x64ress\x18\x02 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:\"address\"\x12I\n\npoolParams\x18\x03 \x01(\x0b\x32\x19.nibiru.dex.v1.PoolParamsB\x1a\xf2\xde\x1f\x12yaml:\"pool_params\"\xc8\xde\x1f\x00\x12H\n\npoolAssets\x18\x04 \x03(\x0b\x32\x18.nibiru.dex.v1.PoolAssetB\x1a\xf2\xde\x1f\x12yaml:\"pool_assets\"\xc8\xde\x1f\x00\x12Z\n\x0btotalWeight\x18\x05 \x01(\tBE\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x13yaml:\"total_weight\"\xc8\xde\x1f\x00\x12K\n\x0btotalShares\x18\x06 \x01(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x1b\xf2\xde\x1f\x13yaml:\"total_shares\"\xc8\xde\x1f\x00:\x04\x88\xa0\x1f\x00\x42+Z)github.com/NibiruChain/nibiru/x/dex/typesb\x06proto3')



_POOLPARAMS = DESCRIPTOR.message_types_by_name['PoolParams']
_POOLASSET = DESCRIPTOR.message_types_by_name['PoolAsset']
_POOL = DESCRIPTOR.message_types_by_name['Pool']
PoolParams = _reflection.GeneratedProtocolMessageType('PoolParams', (_message.Message,), {
  'DESCRIPTOR' : _POOLPARAMS,
  '__module__' : 'dex.v1.pool_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.dex.v1.PoolParams)
  })
_sym_db.RegisterMessage(PoolParams)

PoolAsset = _reflection.GeneratedProtocolMessageType('PoolAsset', (_message.Message,), {
  'DESCRIPTOR' : _POOLASSET,
  '__module__' : 'dex.v1.pool_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.dex.v1.PoolAsset)
  })
_sym_db.RegisterMessage(PoolAsset)

Pool = _reflection.GeneratedProtocolMessageType('Pool', (_message.Message,), {
  'DESCRIPTOR' : _POOL,
  '__module__' : 'dex.v1.pool_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.dex.v1.Pool)
  })
_sym_db.RegisterMessage(Pool)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z)github.com/NibiruChain/nibiru/x/dex/types'
  _POOLPARAMS.fields_by_name['swapFee']._options = None
  _POOLPARAMS.fields_by_name['swapFee']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\362\336\037\017yaml:\"swap_fee\"\310\336\037\000'
  _POOLPARAMS.fields_by_name['exitFee']._options = None
  _POOLPARAMS.fields_by_name['exitFee']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\362\336\037\017yaml:\"exit_fee\"\310\336\037\000'
  _POOLASSET.fields_by_name['token']._options = None
  _POOLASSET.fields_by_name['token']._serialized_options = b'\362\336\037\014yaml:\"token\"\310\336\037\000'
  _POOLASSET.fields_by_name['weight']._options = None
  _POOLASSET.fields_by_name['weight']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Int\362\336\037\ryaml:\"weight\"\310\336\037\000'
  _POOL.fields_by_name['address']._options = None
  _POOL.fields_by_name['address']._serialized_options = b'\362\336\037\016yaml:\"address\"'
  _POOL.fields_by_name['poolParams']._options = None
  _POOL.fields_by_name['poolParams']._serialized_options = b'\362\336\037\022yaml:\"pool_params\"\310\336\037\000'
  _POOL.fields_by_name['poolAssets']._options = None
  _POOL.fields_by_name['poolAssets']._serialized_options = b'\362\336\037\022yaml:\"pool_assets\"\310\336\037\000'
  _POOL.fields_by_name['totalWeight']._options = None
  _POOL.fields_by_name['totalWeight']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Int\362\336\037\023yaml:\"total_weight\"\310\336\037\000'
  _POOL.fields_by_name['totalShares']._options = None
  _POOL.fields_by_name['totalShares']._serialized_options = b'\362\336\037\023yaml:\"total_shares\"\310\336\037\000'
  _POOL._options = None
  _POOL._serialized_options = b'\210\240\037\000'
  _POOLPARAMS._serialized_start=118
  _POOLPARAMS._serialized_end=298
  _POOLASSET._serialized_start=301
  _POOLASSET._serialized_end=457
  _POOL._serialized_start=460
  _POOL._serialized_end=839
# @@protoc_insertion_point(module_scope)
