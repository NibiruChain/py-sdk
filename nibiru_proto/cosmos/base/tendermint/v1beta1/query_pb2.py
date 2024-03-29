# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/base/tendermint/v1beta1/query.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from tendermint.p2p import types_pb2 as tendermint_dot_p2p_dot_types__pb2
from tendermint.types import types_pb2 as tendermint_dot_types_dot_types__pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from cosmos.base.tendermint.v1beta1 import types_pb2 as cosmos_dot_base_dot_tendermint_dot_v1beta1_dot_types__pb2
from cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from tendermint.types import block_pb2 as tendermint_dot_types_dot_block__pb2
from amino import amino_pb2 as amino_dot_amino__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*cosmos/base/tendermint/v1beta1/query.proto\x12\x1e\x63osmos.base.tendermint.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x19google/protobuf/any.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1atendermint/p2p/types.proto\x1a\x1ctendermint/types/types.proto\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a*cosmos/base/tendermint/v1beta1/types.proto\x1a\x19\x63osmos_proto/cosmos.proto\x1a\x1ctendermint/types/block.proto\x1a\x11\x61mino/amino.proto\"\x80\x01\n\x1eGetValidatorSetByHeightRequest\x12\x16\n\x06height\x18\x01 \x01(\x03R\x06height\x12\x46\n\npagination\x18\x02 \x01(\x0b\x32&.cosmos.base.query.v1beta1.PageRequestR\npagination\"\xd8\x01\n\x1fGetValidatorSetByHeightResponse\x12!\n\x0c\x62lock_height\x18\x01 \x01(\x03R\x0b\x62lockHeight\x12I\n\nvalidators\x18\x02 \x03(\x0b\x32).cosmos.base.tendermint.v1beta1.ValidatorR\nvalidators\x12G\n\npagination\x18\x03 \x01(\x0b\x32\'.cosmos.base.query.v1beta1.PageResponseR\npagination\"f\n\x1cGetLatestValidatorSetRequest\x12\x46\n\npagination\x18\x01 \x01(\x0b\x32&.cosmos.base.query.v1beta1.PageRequestR\npagination\"\xd6\x01\n\x1dGetLatestValidatorSetResponse\x12!\n\x0c\x62lock_height\x18\x01 \x01(\x03R\x0b\x62lockHeight\x12I\n\nvalidators\x18\x02 \x03(\x0b\x32).cosmos.base.tendermint.v1beta1.ValidatorR\nvalidators\x12G\n\npagination\x18\x03 \x01(\x0b\x32\'.cosmos.base.query.v1beta1.PageResponseR\npagination\"\xbe\x01\n\tValidator\x12\x32\n\x07\x61\x64\x64ress\x18\x01 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressStringR\x07\x61\x64\x64ress\x12-\n\x07pub_key\x18\x02 \x01(\x0b\x32\x14.google.protobuf.AnyR\x06pubKey\x12!\n\x0cvoting_power\x18\x03 \x01(\x03R\x0bvotingPower\x12+\n\x11proposer_priority\x18\x04 \x01(\x03R\x10proposerPriority\"1\n\x17GetBlockByHeightRequest\x12\x16\n\x06height\x18\x01 \x01(\x03R\x06height\"\xc3\x01\n\x18GetBlockByHeightResponse\x12\x34\n\x08\x62lock_id\x18\x01 \x01(\x0b\x32\x19.tendermint.types.BlockIDR\x07\x62lockId\x12-\n\x05\x62lock\x18\x02 \x01(\x0b\x32\x17.tendermint.types.BlockR\x05\x62lock\x12\x42\n\tsdk_block\x18\x03 \x01(\x0b\x32%.cosmos.base.tendermint.v1beta1.BlockR\x08sdkBlock\"\x17\n\x15GetLatestBlockRequest\"\xc1\x01\n\x16GetLatestBlockResponse\x12\x34\n\x08\x62lock_id\x18\x01 \x01(\x0b\x32\x19.tendermint.types.BlockIDR\x07\x62lockId\x12-\n\x05\x62lock\x18\x02 \x01(\x0b\x32\x17.tendermint.types.BlockR\x05\x62lock\x12\x42\n\tsdk_block\x18\x03 \x01(\x0b\x32%.cosmos.base.tendermint.v1beta1.BlockR\x08sdkBlock\"\x13\n\x11GetSyncingRequest\".\n\x12GetSyncingResponse\x12\x18\n\x07syncing\x18\x01 \x01(\x08R\x07syncing\"\x14\n\x12GetNodeInfoRequest\"\xc0\x01\n\x13GetNodeInfoResponse\x12K\n\x11\x64\x65\x66\x61ult_node_info\x18\x01 \x01(\x0b\x32\x1f.tendermint.p2p.DefaultNodeInfoR\x0f\x64\x65\x66\x61ultNodeInfo\x12\\\n\x13\x61pplication_version\x18\x02 \x01(\x0b\x32+.cosmos.base.tendermint.v1beta1.VersionInfoR\x12\x61pplicationVersion\"\xa8\x02\n\x0bVersionInfo\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x19\n\x08\x61pp_name\x18\x02 \x01(\tR\x07\x61ppName\x12\x18\n\x07version\x18\x03 \x01(\tR\x07version\x12\x1d\n\ngit_commit\x18\x04 \x01(\tR\tgitCommit\x12\x1d\n\nbuild_tags\x18\x05 \x01(\tR\tbuildTags\x12\x1d\n\ngo_version\x18\x06 \x01(\tR\tgoVersion\x12\x45\n\nbuild_deps\x18\x07 \x03(\x0b\x32&.cosmos.base.tendermint.v1beta1.ModuleR\tbuildDeps\x12,\n\x12\x63osmos_sdk_version\x18\x08 \x01(\tR\x10\x63osmosSdkVersion\"H\n\x06Module\x12\x12\n\x04path\x18\x01 \x01(\tR\x04path\x12\x18\n\x07version\x18\x02 \x01(\tR\x07version\x12\x10\n\x03sum\x18\x03 \x01(\tR\x03sum\"h\n\x10\x41\x42\x43IQueryRequest\x12\x12\n\x04\x64\x61ta\x18\x01 \x01(\x0cR\x04\x64\x61ta\x12\x12\n\x04path\x18\x02 \x01(\tR\x04path\x12\x16\n\x06height\x18\x03 \x01(\x03R\x06height\x12\x14\n\x05prove\x18\x04 \x01(\x08R\x05prove\"\x8e\x02\n\x11\x41\x42\x43IQueryResponse\x12\x12\n\x04\x63ode\x18\x01 \x01(\rR\x04\x63ode\x12\x10\n\x03log\x18\x03 \x01(\tR\x03log\x12\x12\n\x04info\x18\x04 \x01(\tR\x04info\x12\x14\n\x05index\x18\x05 \x01(\x03R\x05index\x12\x10\n\x03key\x18\x06 \x01(\x0cR\x03key\x12\x14\n\x05value\x18\x07 \x01(\x0cR\x05value\x12\x45\n\tproof_ops\x18\x08 \x01(\x0b\x32(.cosmos.base.tendermint.v1beta1.ProofOpsR\x08proofOps\x12\x16\n\x06height\x18\t \x01(\x03R\x06height\x12\x1c\n\tcodespace\x18\n \x01(\tR\tcodespaceJ\x04\x08\x02\x10\x03\"C\n\x07ProofOp\x12\x12\n\x04type\x18\x01 \x01(\tR\x04type\x12\x10\n\x03key\x18\x02 \x01(\x0cR\x03key\x12\x12\n\x04\x64\x61ta\x18\x03 \x01(\x0cR\x04\x64\x61ta\"P\n\x08ProofOps\x12\x44\n\x03ops\x18\x01 \x03(\x0b\x32\'.cosmos.base.tendermint.v1beta1.ProofOpB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01R\x03ops2\xaf\n\n\x07Service\x12\xa9\x01\n\x0bGetNodeInfo\x12\x32.cosmos.base.tendermint.v1beta1.GetNodeInfoRequest\x1a\x33.cosmos.base.tendermint.v1beta1.GetNodeInfoResponse\"1\x82\xd3\xe4\x93\x02+\x12)/cosmos/base/tendermint/v1beta1/node_info\x12\xa4\x01\n\nGetSyncing\x12\x31.cosmos.base.tendermint.v1beta1.GetSyncingRequest\x1a\x32.cosmos.base.tendermint.v1beta1.GetSyncingResponse\"/\x82\xd3\xe4\x93\x02)\x12\'/cosmos/base/tendermint/v1beta1/syncing\x12\xb6\x01\n\x0eGetLatestBlock\x12\x35.cosmos.base.tendermint.v1beta1.GetLatestBlockRequest\x1a\x36.cosmos.base.tendermint.v1beta1.GetLatestBlockResponse\"5\x82\xd3\xe4\x93\x02/\x12-/cosmos/base/tendermint/v1beta1/blocks/latest\x12\xbe\x01\n\x10GetBlockByHeight\x12\x37.cosmos.base.tendermint.v1beta1.GetBlockByHeightRequest\x1a\x38.cosmos.base.tendermint.v1beta1.GetBlockByHeightResponse\"7\x82\xd3\xe4\x93\x02\x31\x12//cosmos/base/tendermint/v1beta1/blocks/{height}\x12\xd2\x01\n\x15GetLatestValidatorSet\x12<.cosmos.base.tendermint.v1beta1.GetLatestValidatorSetRequest\x1a=.cosmos.base.tendermint.v1beta1.GetLatestValidatorSetResponse\"<\x82\xd3\xe4\x93\x02\x36\x12\x34/cosmos/base/tendermint/v1beta1/validatorsets/latest\x12\xda\x01\n\x17GetValidatorSetByHeight\x12>.cosmos.base.tendermint.v1beta1.GetValidatorSetByHeightRequest\x1a?.cosmos.base.tendermint.v1beta1.GetValidatorSetByHeightResponse\">\x82\xd3\xe4\x93\x02\x38\x12\x36/cosmos/base/tendermint/v1beta1/validatorsets/{height}\x12\xa4\x01\n\tABCIQuery\x12\x30.cosmos.base.tendermint.v1beta1.ABCIQueryRequest\x1a\x31.cosmos.base.tendermint.v1beta1.ABCIQueryResponse\"2\x82\xd3\xe4\x93\x02,\x12*/cosmos/base/tendermint/v1beta1/abci_queryB4Z2github.com/cosmos/cosmos-sdk/client/grpc/tmserviceb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.base.tendermint.v1beta1.query_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z2github.com/cosmos/cosmos-sdk/client/grpc/tmservice'
  _VALIDATOR.fields_by_name['address']._options = None
  _VALIDATOR.fields_by_name['address']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _PROOFOPS.fields_by_name['ops']._options = None
  _PROOFOPS.fields_by_name['ops']._serialized_options = b'\310\336\037\000\250\347\260*\001'
  _SERVICE.methods_by_name['GetNodeInfo']._options = None
  _SERVICE.methods_by_name['GetNodeInfo']._serialized_options = b'\202\323\344\223\002+\022)/cosmos/base/tendermint/v1beta1/node_info'
  _SERVICE.methods_by_name['GetSyncing']._options = None
  _SERVICE.methods_by_name['GetSyncing']._serialized_options = b'\202\323\344\223\002)\022\'/cosmos/base/tendermint/v1beta1/syncing'
  _SERVICE.methods_by_name['GetLatestBlock']._options = None
  _SERVICE.methods_by_name['GetLatestBlock']._serialized_options = b'\202\323\344\223\002/\022-/cosmos/base/tendermint/v1beta1/blocks/latest'
  _SERVICE.methods_by_name['GetBlockByHeight']._options = None
  _SERVICE.methods_by_name['GetBlockByHeight']._serialized_options = b'\202\323\344\223\0021\022//cosmos/base/tendermint/v1beta1/blocks/{height}'
  _SERVICE.methods_by_name['GetLatestValidatorSet']._options = None
  _SERVICE.methods_by_name['GetLatestValidatorSet']._serialized_options = b'\202\323\344\223\0026\0224/cosmos/base/tendermint/v1beta1/validatorsets/latest'
  _SERVICE.methods_by_name['GetValidatorSetByHeight']._options = None
  _SERVICE.methods_by_name['GetValidatorSetByHeight']._serialized_options = b'\202\323\344\223\0028\0226/cosmos/base/tendermint/v1beta1/validatorsets/{height}'
  _SERVICE.methods_by_name['ABCIQuery']._options = None
  _SERVICE.methods_by_name['ABCIQuery']._serialized_options = b'\202\323\344\223\002,\022*/cosmos/base/tendermint/v1beta1/abci_query'
  _GETVALIDATORSETBYHEIGHTREQUEST._serialized_start=380
  _GETVALIDATORSETBYHEIGHTREQUEST._serialized_end=508
  _GETVALIDATORSETBYHEIGHTRESPONSE._serialized_start=511
  _GETVALIDATORSETBYHEIGHTRESPONSE._serialized_end=727
  _GETLATESTVALIDATORSETREQUEST._serialized_start=729
  _GETLATESTVALIDATORSETREQUEST._serialized_end=831
  _GETLATESTVALIDATORSETRESPONSE._serialized_start=834
  _GETLATESTVALIDATORSETRESPONSE._serialized_end=1048
  _VALIDATOR._serialized_start=1051
  _VALIDATOR._serialized_end=1241
  _GETBLOCKBYHEIGHTREQUEST._serialized_start=1243
  _GETBLOCKBYHEIGHTREQUEST._serialized_end=1292
  _GETBLOCKBYHEIGHTRESPONSE._serialized_start=1295
  _GETBLOCKBYHEIGHTRESPONSE._serialized_end=1490
  _GETLATESTBLOCKREQUEST._serialized_start=1492
  _GETLATESTBLOCKREQUEST._serialized_end=1515
  _GETLATESTBLOCKRESPONSE._serialized_start=1518
  _GETLATESTBLOCKRESPONSE._serialized_end=1711
  _GETSYNCINGREQUEST._serialized_start=1713
  _GETSYNCINGREQUEST._serialized_end=1732
  _GETSYNCINGRESPONSE._serialized_start=1734
  _GETSYNCINGRESPONSE._serialized_end=1780
  _GETNODEINFOREQUEST._serialized_start=1782
  _GETNODEINFOREQUEST._serialized_end=1802
  _GETNODEINFORESPONSE._serialized_start=1805
  _GETNODEINFORESPONSE._serialized_end=1997
  _VERSIONINFO._serialized_start=2000
  _VERSIONINFO._serialized_end=2296
  _MODULE._serialized_start=2298
  _MODULE._serialized_end=2370
  _ABCIQUERYREQUEST._serialized_start=2372
  _ABCIQUERYREQUEST._serialized_end=2476
  _ABCIQUERYRESPONSE._serialized_start=2479
  _ABCIQUERYRESPONSE._serialized_end=2749
  _PROOFOP._serialized_start=2751
  _PROOFOP._serialized_end=2818
  _PROOFOPS._serialized_start=2820
  _PROOFOPS._serialized_end=2900
  _SERVICE._serialized_start=2903
  _SERVICE._serialized_end=4230
# @@protoc_insertion_point(module_scope)
