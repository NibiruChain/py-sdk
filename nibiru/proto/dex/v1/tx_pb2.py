# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dex/v1/tx.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from dex.v1 import params_pb2 as dex_dot_v1_dot_params__pb2
from dex.v1 import pool_pb2 as dex_dot_v1_dot_pool__pb2
from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x64\x65x/v1/tx.proto\x12\rnibiru.dex.v1\x1a\x13\x64\x65x/v1/params.proto\x1a\x11\x64\x65x/v1/pool.proto\x1a\x14gogoproto/gogo.proto\x1a\x1e\x63osmos/base/v1beta1/coin.proto\x1a\x1cgoogle/api/annotations.proto\"\x9b\x01\n\rMsgCreatePool\x12\x0f\n\x07\x63reator\x18\x01 \x01(\t\x12\x45\n\npoolParams\x18\x02 \x01(\x0b\x32\x19.nibiru.dex.v1.PoolParamsB\x16\xf2\xde\x1f\x12yaml:\"pool_params\"\x12\x32\n\npoolAssets\x18\x03 \x03(\x0b\x32\x18.nibiru.dex.v1.PoolAssetB\x04\xc8\xde\x1f\x00\"\'\n\x15MsgCreatePoolResponse\x12\x0e\n\x06poolId\x18\x01 \x01(\x04\"\x9b\x01\n\x0bMsgJoinPool\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:\"sender\"\x12\"\n\x06poolId\x18\x02 \x01(\x04\x42\x12\xf2\xde\x1f\x0eyaml:\"pool_id\"\x12\x45\n\x08tokensIn\x18\x03 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x18\xf2\xde\x1f\x10yaml:\"tokens_in\"\xc8\xde\x1f\x00\"\xde\x01\n\x13MsgJoinPoolResponse\x12!\n\x04pool\x18\x01 \x01(\x0b\x32\x13.nibiru.dex.v1.Pool\x12W\n\x10numPoolSharesOut\x18\x02 \x01(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\"\xf2\xde\x1f\x1ayaml:\"num_pool_shares_out\"\xc8\xde\x1f\x00\x12K\n\x0eremainingCoins\x18\x03 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x18\xf2\xde\x1f\x10yaml:\"tokens_in\"\xc8\xde\x1f\x00\"\x9f\x01\n\x0bMsgExitPool\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:\"sender\"\x12\"\n\x06poolId\x18\x02 \x01(\x04\x42\x12\xf2\xde\x1f\x0eyaml:\"pool_id\"\x12I\n\npoolShares\x18\x03 \x01(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x1a\xf2\xde\x1f\x12yaml:\"pool_shares\"\xc8\xde\x1f\x00\"^\n\x13MsgExitPoolResponse\x12G\n\ttokensOut\x18\x03 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x19\xf2\xde\x1f\x11yaml:\"tokens_out\"\xc8\xde\x1f\x00\"\xce\x01\n\rMsgSwapAssets\x12!\n\x06sender\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:\"sender\"\x12\"\n\x06poolId\x18\x02 \x01(\x04\x42\x12\xf2\xde\x1f\x0eyaml:\"pool_id\"\x12\x43\n\x07tokenIn\x18\x03 \x01(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x17\xf2\xde\x1f\x0fyaml:\"token_in\"\xc8\xde\x1f\x00\x12\x31\n\rtokenOutDenom\x18\x04 \x01(\tB\x1a\xf2\xde\x1f\x16yaml:\"token_out_denom\"\"^\n\x15MsgSwapAssetsResponse\x12\x45\n\x08tokenOut\x18\x03 \x01(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x18\xf2\xde\x1f\x10yaml:\"token_out\"\xc8\xde\x1f\x00\"\xd5\x01\n\x0f\x45ventPoolJoined\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x0f\n\x07pool_id\x18\x02 \x01(\x04\x12\x32\n\ttokens_in\x18\x03 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00\x12\x38\n\x0fpool_shares_out\x18\x04 \x01(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00\x12\x32\n\trem_coins\x18\x05 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00\"4\n\x10\x45ventPoolCreated\x12\x0f\n\x07\x63reator\x18\x01 \x01(\t\x12\x0f\n\x07pool_id\x18\x02 \x01(\x04\"\xa1\x01\n\x0f\x45ventPoolExited\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x0f\n\x07pool_id\x18\x02 \x01(\x04\x12\x37\n\x0epool_shares_in\x18\x03 \x01(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00\x12\x33\n\ntokens_out\x18\x04 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00\"\x9d\x01\n\x12\x45ventAssetsSwapped\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x0f\n\x07pool_id\x18\x02 \x01(\x04\x12\x31\n\x08token_in\x18\x03 \x01(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00\x12\x32\n\ttoken_out\x18\x04 \x01(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00\x32\xc4\x03\n\x03Msg\x12j\n\nCreatePool\x12\x1c.nibiru.dex.v1.MsgCreatePool\x1a$.nibiru.dex.v1.MsgCreatePoolResponse\"\x18\x82\xd3\xe4\x93\x02\x12\"\x10/nibiru/dex/pool\x12m\n\x08JoinPool\x12\x1a.nibiru.dex.v1.MsgJoinPool\x1a\".nibiru.dex.v1.MsgJoinPoolResponse\"!\x82\xd3\xe4\x93\x02\x1b\"\x19/nibiru/dex/{poolId}/join\x12m\n\x08\x45xitPool\x12\x1a.nibiru.dex.v1.MsgExitPool\x1a\".nibiru.dex.v1.MsgExitPoolResponse\"!\x82\xd3\xe4\x93\x02\x1b\"\x19/nibiru/dex/{poolId}/exit\x12s\n\nSwapAssets\x12\x1c.nibiru.dex.v1.MsgSwapAssets\x1a$.nibiru.dex.v1.MsgSwapAssetsResponse\"!\x82\xd3\xe4\x93\x02\x1b\"\x19/nibiru/dex/{poolId}/swapB+Z)github.com/NibiruChain/nibiru/x/dex/typesb\x06proto3')



_MSGCREATEPOOL = DESCRIPTOR.message_types_by_name['MsgCreatePool']
_MSGCREATEPOOLRESPONSE = DESCRIPTOR.message_types_by_name['MsgCreatePoolResponse']
_MSGJOINPOOL = DESCRIPTOR.message_types_by_name['MsgJoinPool']
_MSGJOINPOOLRESPONSE = DESCRIPTOR.message_types_by_name['MsgJoinPoolResponse']
_MSGEXITPOOL = DESCRIPTOR.message_types_by_name['MsgExitPool']
_MSGEXITPOOLRESPONSE = DESCRIPTOR.message_types_by_name['MsgExitPoolResponse']
_MSGSWAPASSETS = DESCRIPTOR.message_types_by_name['MsgSwapAssets']
_MSGSWAPASSETSRESPONSE = DESCRIPTOR.message_types_by_name['MsgSwapAssetsResponse']
_EVENTPOOLJOINED = DESCRIPTOR.message_types_by_name['EventPoolJoined']
_EVENTPOOLCREATED = DESCRIPTOR.message_types_by_name['EventPoolCreated']
_EVENTPOOLEXITED = DESCRIPTOR.message_types_by_name['EventPoolExited']
_EVENTASSETSSWAPPED = DESCRIPTOR.message_types_by_name['EventAssetsSwapped']
MsgCreatePool = _reflection.GeneratedProtocolMessageType('MsgCreatePool', (_message.Message,), {
  'DESCRIPTOR' : _MSGCREATEPOOL,
  '__module__' : 'dex.v1.tx_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.dex.v1.MsgCreatePool)
  })
_sym_db.RegisterMessage(MsgCreatePool)

MsgCreatePoolResponse = _reflection.GeneratedProtocolMessageType('MsgCreatePoolResponse', (_message.Message,), {
  'DESCRIPTOR' : _MSGCREATEPOOLRESPONSE,
  '__module__' : 'dex.v1.tx_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.dex.v1.MsgCreatePoolResponse)
  })
_sym_db.RegisterMessage(MsgCreatePoolResponse)

MsgJoinPool = _reflection.GeneratedProtocolMessageType('MsgJoinPool', (_message.Message,), {
  'DESCRIPTOR' : _MSGJOINPOOL,
  '__module__' : 'dex.v1.tx_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.dex.v1.MsgJoinPool)
  })
_sym_db.RegisterMessage(MsgJoinPool)

MsgJoinPoolResponse = _reflection.GeneratedProtocolMessageType('MsgJoinPoolResponse', (_message.Message,), {
  'DESCRIPTOR' : _MSGJOINPOOLRESPONSE,
  '__module__' : 'dex.v1.tx_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.dex.v1.MsgJoinPoolResponse)
  })
_sym_db.RegisterMessage(MsgJoinPoolResponse)

MsgExitPool = _reflection.GeneratedProtocolMessageType('MsgExitPool', (_message.Message,), {
  'DESCRIPTOR' : _MSGEXITPOOL,
  '__module__' : 'dex.v1.tx_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.dex.v1.MsgExitPool)
  })
_sym_db.RegisterMessage(MsgExitPool)

MsgExitPoolResponse = _reflection.GeneratedProtocolMessageType('MsgExitPoolResponse', (_message.Message,), {
  'DESCRIPTOR' : _MSGEXITPOOLRESPONSE,
  '__module__' : 'dex.v1.tx_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.dex.v1.MsgExitPoolResponse)
  })
_sym_db.RegisterMessage(MsgExitPoolResponse)

MsgSwapAssets = _reflection.GeneratedProtocolMessageType('MsgSwapAssets', (_message.Message,), {
  'DESCRIPTOR' : _MSGSWAPASSETS,
  '__module__' : 'dex.v1.tx_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.dex.v1.MsgSwapAssets)
  })
_sym_db.RegisterMessage(MsgSwapAssets)

MsgSwapAssetsResponse = _reflection.GeneratedProtocolMessageType('MsgSwapAssetsResponse', (_message.Message,), {
  'DESCRIPTOR' : _MSGSWAPASSETSRESPONSE,
  '__module__' : 'dex.v1.tx_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.dex.v1.MsgSwapAssetsResponse)
  })
_sym_db.RegisterMessage(MsgSwapAssetsResponse)

EventPoolJoined = _reflection.GeneratedProtocolMessageType('EventPoolJoined', (_message.Message,), {
  'DESCRIPTOR' : _EVENTPOOLJOINED,
  '__module__' : 'dex.v1.tx_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.dex.v1.EventPoolJoined)
  })
_sym_db.RegisterMessage(EventPoolJoined)

EventPoolCreated = _reflection.GeneratedProtocolMessageType('EventPoolCreated', (_message.Message,), {
  'DESCRIPTOR' : _EVENTPOOLCREATED,
  '__module__' : 'dex.v1.tx_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.dex.v1.EventPoolCreated)
  })
_sym_db.RegisterMessage(EventPoolCreated)

EventPoolExited = _reflection.GeneratedProtocolMessageType('EventPoolExited', (_message.Message,), {
  'DESCRIPTOR' : _EVENTPOOLEXITED,
  '__module__' : 'dex.v1.tx_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.dex.v1.EventPoolExited)
  })
_sym_db.RegisterMessage(EventPoolExited)

EventAssetsSwapped = _reflection.GeneratedProtocolMessageType('EventAssetsSwapped', (_message.Message,), {
  'DESCRIPTOR' : _EVENTASSETSSWAPPED,
  '__module__' : 'dex.v1.tx_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.dex.v1.EventAssetsSwapped)
  })
_sym_db.RegisterMessage(EventAssetsSwapped)

_MSG = DESCRIPTOR.services_by_name['Msg']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z)github.com/NibiruChain/nibiru/x/dex/types'
  _MSGCREATEPOOL.fields_by_name['poolParams']._options = None
  _MSGCREATEPOOL.fields_by_name['poolParams']._serialized_options = b'\362\336\037\022yaml:\"pool_params\"'
  _MSGCREATEPOOL.fields_by_name['poolAssets']._options = None
  _MSGCREATEPOOL.fields_by_name['poolAssets']._serialized_options = b'\310\336\037\000'
  _MSGJOINPOOL.fields_by_name['sender']._options = None
  _MSGJOINPOOL.fields_by_name['sender']._serialized_options = b'\362\336\037\ryaml:\"sender\"'
  _MSGJOINPOOL.fields_by_name['poolId']._options = None
  _MSGJOINPOOL.fields_by_name['poolId']._serialized_options = b'\362\336\037\016yaml:\"pool_id\"'
  _MSGJOINPOOL.fields_by_name['tokensIn']._options = None
  _MSGJOINPOOL.fields_by_name['tokensIn']._serialized_options = b'\362\336\037\020yaml:\"tokens_in\"\310\336\037\000'
  _MSGJOINPOOLRESPONSE.fields_by_name['numPoolSharesOut']._options = None
  _MSGJOINPOOLRESPONSE.fields_by_name['numPoolSharesOut']._serialized_options = b'\362\336\037\032yaml:\"num_pool_shares_out\"\310\336\037\000'
  _MSGJOINPOOLRESPONSE.fields_by_name['remainingCoins']._options = None
  _MSGJOINPOOLRESPONSE.fields_by_name['remainingCoins']._serialized_options = b'\362\336\037\020yaml:\"tokens_in\"\310\336\037\000'
  _MSGEXITPOOL.fields_by_name['sender']._options = None
  _MSGEXITPOOL.fields_by_name['sender']._serialized_options = b'\362\336\037\ryaml:\"sender\"'
  _MSGEXITPOOL.fields_by_name['poolId']._options = None
  _MSGEXITPOOL.fields_by_name['poolId']._serialized_options = b'\362\336\037\016yaml:\"pool_id\"'
  _MSGEXITPOOL.fields_by_name['poolShares']._options = None
  _MSGEXITPOOL.fields_by_name['poolShares']._serialized_options = b'\362\336\037\022yaml:\"pool_shares\"\310\336\037\000'
  _MSGEXITPOOLRESPONSE.fields_by_name['tokensOut']._options = None
  _MSGEXITPOOLRESPONSE.fields_by_name['tokensOut']._serialized_options = b'\362\336\037\021yaml:\"tokens_out\"\310\336\037\000'
  _MSGSWAPASSETS.fields_by_name['sender']._options = None
  _MSGSWAPASSETS.fields_by_name['sender']._serialized_options = b'\362\336\037\ryaml:\"sender\"'
  _MSGSWAPASSETS.fields_by_name['poolId']._options = None
  _MSGSWAPASSETS.fields_by_name['poolId']._serialized_options = b'\362\336\037\016yaml:\"pool_id\"'
  _MSGSWAPASSETS.fields_by_name['tokenIn']._options = None
  _MSGSWAPASSETS.fields_by_name['tokenIn']._serialized_options = b'\362\336\037\017yaml:\"token_in\"\310\336\037\000'
  _MSGSWAPASSETS.fields_by_name['tokenOutDenom']._options = None
  _MSGSWAPASSETS.fields_by_name['tokenOutDenom']._serialized_options = b'\362\336\037\026yaml:\"token_out_denom\"'
  _MSGSWAPASSETSRESPONSE.fields_by_name['tokenOut']._options = None
  _MSGSWAPASSETSRESPONSE.fields_by_name['tokenOut']._serialized_options = b'\362\336\037\020yaml:\"token_out\"\310\336\037\000'
  _EVENTPOOLJOINED.fields_by_name['tokens_in']._options = None
  _EVENTPOOLJOINED.fields_by_name['tokens_in']._serialized_options = b'\310\336\037\000'
  _EVENTPOOLJOINED.fields_by_name['pool_shares_out']._options = None
  _EVENTPOOLJOINED.fields_by_name['pool_shares_out']._serialized_options = b'\310\336\037\000'
  _EVENTPOOLJOINED.fields_by_name['rem_coins']._options = None
  _EVENTPOOLJOINED.fields_by_name['rem_coins']._serialized_options = b'\310\336\037\000'
  _EVENTPOOLEXITED.fields_by_name['pool_shares_in']._options = None
  _EVENTPOOLEXITED.fields_by_name['pool_shares_in']._serialized_options = b'\310\336\037\000'
  _EVENTPOOLEXITED.fields_by_name['tokens_out']._options = None
  _EVENTPOOLEXITED.fields_by_name['tokens_out']._serialized_options = b'\310\336\037\000'
  _EVENTASSETSSWAPPED.fields_by_name['token_in']._options = None
  _EVENTASSETSSWAPPED.fields_by_name['token_in']._serialized_options = b'\310\336\037\000'
  _EVENTASSETSSWAPPED.fields_by_name['token_out']._options = None
  _EVENTASSETSSWAPPED.fields_by_name['token_out']._serialized_options = b'\310\336\037\000'
  _MSG.methods_by_name['CreatePool']._options = None
  _MSG.methods_by_name['CreatePool']._serialized_options = b'\202\323\344\223\002\022\"\020/nibiru/dex/pool'
  _MSG.methods_by_name['JoinPool']._options = None
  _MSG.methods_by_name['JoinPool']._serialized_options = b'\202\323\344\223\002\033\"\031/nibiru/dex/{poolId}/join'
  _MSG.methods_by_name['ExitPool']._options = None
  _MSG.methods_by_name['ExitPool']._serialized_options = b'\202\323\344\223\002\033\"\031/nibiru/dex/{poolId}/exit'
  _MSG.methods_by_name['SwapAssets']._options = None
  _MSG.methods_by_name['SwapAssets']._serialized_options = b'\202\323\344\223\002\033\"\031/nibiru/dex/{poolId}/swap'
  _MSGCREATEPOOL._serialized_start=159
  _MSGCREATEPOOL._serialized_end=314
  _MSGCREATEPOOLRESPONSE._serialized_start=316
  _MSGCREATEPOOLRESPONSE._serialized_end=355
  _MSGJOINPOOL._serialized_start=358
  _MSGJOINPOOL._serialized_end=513
  _MSGJOINPOOLRESPONSE._serialized_start=516
  _MSGJOINPOOLRESPONSE._serialized_end=738
  _MSGEXITPOOL._serialized_start=741
  _MSGEXITPOOL._serialized_end=900
  _MSGEXITPOOLRESPONSE._serialized_start=902
  _MSGEXITPOOLRESPONSE._serialized_end=996
  _MSGSWAPASSETS._serialized_start=999
  _MSGSWAPASSETS._serialized_end=1205
  _MSGSWAPASSETSRESPONSE._serialized_start=1207
  _MSGSWAPASSETSRESPONSE._serialized_end=1301
  _EVENTPOOLJOINED._serialized_start=1304
  _EVENTPOOLJOINED._serialized_end=1517
  _EVENTPOOLCREATED._serialized_start=1519
  _EVENTPOOLCREATED._serialized_end=1571
  _EVENTPOOLEXITED._serialized_start=1574
  _EVENTPOOLEXITED._serialized_end=1735
  _EVENTASSETSSWAPPED._serialized_start=1738
  _EVENTASSETSSWAPPED._serialized_end=1895
  _MSG._serialized_start=1898
  _MSG._serialized_end=2350
# @@protoc_insertion_point(module_scope)
