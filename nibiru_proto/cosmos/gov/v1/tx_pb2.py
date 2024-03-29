# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/gov/v1/tx.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from cosmos.gov.v1 import gov_pb2 as cosmos_dot_gov_dot_v1_dot_gov__pb2
from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from cosmos.msg.v1 import msg_pb2 as cosmos_dot_msg_dot_v1_dot_msg__pb2
from amino import amino_pb2 as amino_dot_amino__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16\x63osmos/gov/v1/tx.proto\x12\rcosmos.gov.v1\x1a\x1e\x63osmos/base/v1beta1/coin.proto\x1a\x17\x63osmos/gov/v1/gov.proto\x1a\x14gogoproto/gogo.proto\x1a\x19\x63osmos_proto/cosmos.proto\x1a\x19google/protobuf/any.proto\x1a\x17\x63osmos/msg/v1/msg.proto\x1a\x11\x61mino/amino.proto\"\xc9\x02\n\x11MsgSubmitProposal\x12\x30\n\x08messages\x18\x01 \x03(\x0b\x32\x14.google.protobuf.AnyR\x08messages\x12M\n\x0finitial_deposit\x18\x02 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01R\x0einitialDeposit\x12\x34\n\x08proposer\x18\x03 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressStringR\x08proposer\x12\x1a\n\x08metadata\x18\x04 \x01(\tR\x08metadata\x12\x14\n\x05title\x18\x05 \x01(\tR\x05title\x12\x18\n\x07summary\x18\x06 \x01(\tR\x07summary:1\x82\xe7\xb0*\x08proposer\x8a\xe7\xb0*\x1f\x63osmos-sdk/v1/MsgSubmitProposal\"<\n\x19MsgSubmitProposalResponse\x12\x1f\n\x0bproposal_id\x18\x01 \x01(\x04R\nproposalId\"\xbb\x01\n\x14MsgExecLegacyContent\x12N\n\x07\x63ontent\x18\x01 \x01(\x0b\x32\x14.google.protobuf.AnyB\x1e\xca\xb4-\x1a\x63osmos.gov.v1beta1.ContentR\x07\x63ontent\x12\x1c\n\tauthority\x18\x02 \x01(\tR\tauthority:5\x82\xe7\xb0*\tauthority\x8a\xe7\xb0*\"cosmos-sdk/v1/MsgExecLegacyContent\"\x1e\n\x1cMsgExecLegacyContentResponse\"\xe5\x01\n\x07MsgVote\x12\x35\n\x0bproposal_id\x18\x01 \x01(\x04\x42\x14\xea\xde\x1f\x0bproposal_id\xa8\xe7\xb0*\x01R\nproposalId\x12.\n\x05voter\x18\x02 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressStringR\x05voter\x12\x31\n\x06option\x18\x03 \x01(\x0e\x32\x19.cosmos.gov.v1.VoteOptionR\x06option\x12\x1a\n\x08metadata\x18\x04 \x01(\tR\x08metadata:$\x82\xe7\xb0*\x05voter\x8a\xe7\xb0*\x15\x63osmos-sdk/v1/MsgVote\"\x11\n\x0fMsgVoteResponse\"\xff\x01\n\x0fMsgVoteWeighted\x12\x35\n\x0bproposal_id\x18\x01 \x01(\x04\x42\x14\xea\xde\x1f\x0bproposal_id\xa8\xe7\xb0*\x01R\nproposalId\x12.\n\x05voter\x18\x02 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressStringR\x05voter\x12;\n\x07options\x18\x03 \x03(\x0b\x32!.cosmos.gov.v1.WeightedVoteOptionR\x07options\x12\x1a\n\x08metadata\x18\x04 \x01(\tR\x08metadata:,\x82\xe7\xb0*\x05voter\x8a\xe7\xb0*\x1d\x63osmos-sdk/v1/MsgVoteWeighted\"\x19\n\x17MsgVoteWeightedResponse\"\xe6\x01\n\nMsgDeposit\x12\x35\n\x0bproposal_id\x18\x01 \x01(\x04\x42\x14\xea\xde\x1f\x0bproposal_id\xa8\xe7\xb0*\x01R\nproposalId\x12\x36\n\tdepositor\x18\x02 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressStringR\tdepositor\x12<\n\x06\x61mount\x18\x03 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01R\x06\x61mount:+\x82\xe7\xb0*\tdepositor\x8a\xe7\xb0*\x18\x63osmos-sdk/v1/MsgDeposit\"\x14\n\x12MsgDepositResponse\"\xbb\x01\n\x0fMsgUpdateParams\x12\x36\n\tauthority\x18\x01 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressStringR\tauthority\x12\x38\n\x06params\x18\x02 \x01(\x0b\x32\x15.cosmos.gov.v1.ParamsB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01R\x06params:6\x82\xe7\xb0*\tauthority\x8a\xe7\xb0*#cosmos-sdk/x/gov/v1/MsgUpdateParams\"\x19\n\x17MsgUpdateParamsResponse2\x8a\x04\n\x03Msg\x12\\\n\x0eSubmitProposal\x12 .cosmos.gov.v1.MsgSubmitProposal\x1a(.cosmos.gov.v1.MsgSubmitProposalResponse\x12\x65\n\x11\x45xecLegacyContent\x12#.cosmos.gov.v1.MsgExecLegacyContent\x1a+.cosmos.gov.v1.MsgExecLegacyContentResponse\x12>\n\x04Vote\x12\x16.cosmos.gov.v1.MsgVote\x1a\x1e.cosmos.gov.v1.MsgVoteResponse\x12V\n\x0cVoteWeighted\x12\x1e.cosmos.gov.v1.MsgVoteWeighted\x1a&.cosmos.gov.v1.MsgVoteWeightedResponse\x12G\n\x07\x44\x65posit\x12\x19.cosmos.gov.v1.MsgDeposit\x1a!.cosmos.gov.v1.MsgDepositResponse\x12V\n\x0cUpdateParams\x12\x1e.cosmos.gov.v1.MsgUpdateParams\x1a&.cosmos.gov.v1.MsgUpdateParamsResponse\x1a\x05\x80\xe7\xb0*\x01\x42-Z+github.com/cosmos/cosmos-sdk/x/gov/types/v1b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.gov.v1.tx_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z+github.com/cosmos/cosmos-sdk/x/gov/types/v1'
  _MSGSUBMITPROPOSAL.fields_by_name['initial_deposit']._options = None
  _MSGSUBMITPROPOSAL.fields_by_name['initial_deposit']._serialized_options = b'\310\336\037\000\250\347\260*\001'
  _MSGSUBMITPROPOSAL.fields_by_name['proposer']._options = None
  _MSGSUBMITPROPOSAL.fields_by_name['proposer']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _MSGSUBMITPROPOSAL._options = None
  _MSGSUBMITPROPOSAL._serialized_options = b'\202\347\260*\010proposer\212\347\260*\037cosmos-sdk/v1/MsgSubmitProposal'
  _MSGEXECLEGACYCONTENT.fields_by_name['content']._options = None
  _MSGEXECLEGACYCONTENT.fields_by_name['content']._serialized_options = b'\312\264-\032cosmos.gov.v1beta1.Content'
  _MSGEXECLEGACYCONTENT._options = None
  _MSGEXECLEGACYCONTENT._serialized_options = b'\202\347\260*\tauthority\212\347\260*\"cosmos-sdk/v1/MsgExecLegacyContent'
  _MSGVOTE.fields_by_name['proposal_id']._options = None
  _MSGVOTE.fields_by_name['proposal_id']._serialized_options = b'\352\336\037\013proposal_id\250\347\260*\001'
  _MSGVOTE.fields_by_name['voter']._options = None
  _MSGVOTE.fields_by_name['voter']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _MSGVOTE._options = None
  _MSGVOTE._serialized_options = b'\202\347\260*\005voter\212\347\260*\025cosmos-sdk/v1/MsgVote'
  _MSGVOTEWEIGHTED.fields_by_name['proposal_id']._options = None
  _MSGVOTEWEIGHTED.fields_by_name['proposal_id']._serialized_options = b'\352\336\037\013proposal_id\250\347\260*\001'
  _MSGVOTEWEIGHTED.fields_by_name['voter']._options = None
  _MSGVOTEWEIGHTED.fields_by_name['voter']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _MSGVOTEWEIGHTED._options = None
  _MSGVOTEWEIGHTED._serialized_options = b'\202\347\260*\005voter\212\347\260*\035cosmos-sdk/v1/MsgVoteWeighted'
  _MSGDEPOSIT.fields_by_name['proposal_id']._options = None
  _MSGDEPOSIT.fields_by_name['proposal_id']._serialized_options = b'\352\336\037\013proposal_id\250\347\260*\001'
  _MSGDEPOSIT.fields_by_name['depositor']._options = None
  _MSGDEPOSIT.fields_by_name['depositor']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _MSGDEPOSIT.fields_by_name['amount']._options = None
  _MSGDEPOSIT.fields_by_name['amount']._serialized_options = b'\310\336\037\000\250\347\260*\001'
  _MSGDEPOSIT._options = None
  _MSGDEPOSIT._serialized_options = b'\202\347\260*\tdepositor\212\347\260*\030cosmos-sdk/v1/MsgDeposit'
  _MSGUPDATEPARAMS.fields_by_name['authority']._options = None
  _MSGUPDATEPARAMS.fields_by_name['authority']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _MSGUPDATEPARAMS.fields_by_name['params']._options = None
  _MSGUPDATEPARAMS.fields_by_name['params']._serialized_options = b'\310\336\037\000\250\347\260*\001'
  _MSGUPDATEPARAMS._options = None
  _MSGUPDATEPARAMS._serialized_options = b'\202\347\260*\tauthority\212\347\260*#cosmos-sdk/x/gov/v1/MsgUpdateParams'
  _MSG._options = None
  _MSG._serialized_options = b'\200\347\260*\001'
  _MSGSUBMITPROPOSAL._serialized_start=219
  _MSGSUBMITPROPOSAL._serialized_end=548
  _MSGSUBMITPROPOSALRESPONSE._serialized_start=550
  _MSGSUBMITPROPOSALRESPONSE._serialized_end=610
  _MSGEXECLEGACYCONTENT._serialized_start=613
  _MSGEXECLEGACYCONTENT._serialized_end=800
  _MSGEXECLEGACYCONTENTRESPONSE._serialized_start=802
  _MSGEXECLEGACYCONTENTRESPONSE._serialized_end=832
  _MSGVOTE._serialized_start=835
  _MSGVOTE._serialized_end=1064
  _MSGVOTERESPONSE._serialized_start=1066
  _MSGVOTERESPONSE._serialized_end=1083
  _MSGVOTEWEIGHTED._serialized_start=1086
  _MSGVOTEWEIGHTED._serialized_end=1341
  _MSGVOTEWEIGHTEDRESPONSE._serialized_start=1343
  _MSGVOTEWEIGHTEDRESPONSE._serialized_end=1368
  _MSGDEPOSIT._serialized_start=1371
  _MSGDEPOSIT._serialized_end=1601
  _MSGDEPOSITRESPONSE._serialized_start=1603
  _MSGDEPOSITRESPONSE._serialized_end=1623
  _MSGUPDATEPARAMS._serialized_start=1626
  _MSGUPDATEPARAMS._serialized_end=1813
  _MSGUPDATEPARAMSRESPONSE._serialized_start=1815
  _MSGUPDATEPARAMSRESPONSE._serialized_end=1840
  _MSG._serialized_start=1843
  _MSG._serialized_end=2365
# @@protoc_insertion_point(module_scope)
