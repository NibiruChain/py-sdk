# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: oracle/v1beta1/tx.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x17oracle/v1beta1/tx.proto\x12\x15nibiru.oracle.v1beta1\x1a\x14gogoproto/gogo.proto\"\x96\x01\n\x1fMsgAggregateExchangeRatePrevote\x12\x1d\n\x04hash\x18\x01 \x01(\tB\x0f\xf2\xde\x1f\x0byaml:\"hash\"\x12!\n\x06\x66\x65\x65\x64\x65r\x18\x02 \x01(\tB\x11\xf2\xde\x1f\ryaml:\"feeder\"\x12\'\n\tvalidator\x18\x03 \x01(\tB\x14\xf2\xde\x1f\x10yaml:\"validator\":\x08\xe8\xa0\x1f\x00\x88\xa0\x1f\x00\")\n\'MsgAggregateExchangeRatePrevoteResponse\"\xc6\x01\n\x1cMsgAggregateExchangeRateVote\x12\x1d\n\x04salt\x18\x01 \x01(\tB\x0f\xf2\xde\x1f\x0byaml:\"salt\"\x12\x31\n\x0e\x65xchange_rates\x18\x02 \x01(\tB\x19\xf2\xde\x1f\x15yaml:\"exchange_rates\"\x12!\n\x06\x66\x65\x65\x64\x65r\x18\x03 \x01(\tB\x11\xf2\xde\x1f\ryaml:\"feeder\"\x12\'\n\tvalidator\x18\x04 \x01(\tB\x14\xf2\xde\x1f\x10yaml:\"validator\":\x08\xe8\xa0\x1f\x00\x88\xa0\x1f\x00\"&\n$MsgAggregateExchangeRateVoteResponse\"p\n\x16MsgDelegateFeedConsent\x12%\n\x08operator\x18\x01 \x01(\tB\x13\xf2\xde\x1f\x0fyaml:\"operator\"\x12%\n\x08\x64\x65legate\x18\x02 \x01(\tB\x13\xf2\xde\x1f\x0fyaml:\"delegate\":\x08\xe8\xa0\x1f\x00\x88\xa0\x1f\x00\" \n\x1eMsgDelegateFeedConsentResponse2\xab\x03\n\x03Msg\x12\x96\x01\n\x1c\x41ggregateExchangeRatePrevote\x12\x36.nibiru.oracle.v1beta1.MsgAggregateExchangeRatePrevote\x1a>.nibiru.oracle.v1beta1.MsgAggregateExchangeRatePrevoteResponse\x12\x8d\x01\n\x19\x41ggregateExchangeRateVote\x12\x33.nibiru.oracle.v1beta1.MsgAggregateExchangeRateVote\x1a;.nibiru.oracle.v1beta1.MsgAggregateExchangeRateVoteResponse\x12{\n\x13\x44\x65legateFeedConsent\x12-.nibiru.oracle.v1beta1.MsgDelegateFeedConsent\x1a\x35.nibiru.oracle.v1beta1.MsgDelegateFeedConsentResponseB.Z,github.com/NibiruChain/nibiru/x/oracle/typesb\x06proto3'
)


_MSGAGGREGATEEXCHANGERATEPREVOTE = DESCRIPTOR.message_types_by_name['MsgAggregateExchangeRatePrevote']
_MSGAGGREGATEEXCHANGERATEPREVOTERESPONSE = DESCRIPTOR.message_types_by_name['MsgAggregateExchangeRatePrevoteResponse']
_MSGAGGREGATEEXCHANGERATEVOTE = DESCRIPTOR.message_types_by_name['MsgAggregateExchangeRateVote']
_MSGAGGREGATEEXCHANGERATEVOTERESPONSE = DESCRIPTOR.message_types_by_name['MsgAggregateExchangeRateVoteResponse']
_MSGDELEGATEFEEDCONSENT = DESCRIPTOR.message_types_by_name['MsgDelegateFeedConsent']
_MSGDELEGATEFEEDCONSENTRESPONSE = DESCRIPTOR.message_types_by_name['MsgDelegateFeedConsentResponse']
MsgAggregateExchangeRatePrevote = _reflection.GeneratedProtocolMessageType(
    'MsgAggregateExchangeRatePrevote',
    (_message.Message,),
    {
        'DESCRIPTOR': _MSGAGGREGATEEXCHANGERATEPREVOTE,
        '__module__': 'oracle.v1beta1.tx_pb2'
        # @@protoc_insertion_point(class_scope:nibiru.oracle.v1beta1.MsgAggregateExchangeRatePrevote)
    },
)
_sym_db.RegisterMessage(MsgAggregateExchangeRatePrevote)

MsgAggregateExchangeRatePrevoteResponse = _reflection.GeneratedProtocolMessageType(
    'MsgAggregateExchangeRatePrevoteResponse',
    (_message.Message,),
    {
        'DESCRIPTOR': _MSGAGGREGATEEXCHANGERATEPREVOTERESPONSE,
        '__module__': 'oracle.v1beta1.tx_pb2'
        # @@protoc_insertion_point(class_scope:nibiru.oracle.v1beta1.MsgAggregateExchangeRatePrevoteResponse)
    },
)
_sym_db.RegisterMessage(MsgAggregateExchangeRatePrevoteResponse)

MsgAggregateExchangeRateVote = _reflection.GeneratedProtocolMessageType(
    'MsgAggregateExchangeRateVote',
    (_message.Message,),
    {
        'DESCRIPTOR': _MSGAGGREGATEEXCHANGERATEVOTE,
        '__module__': 'oracle.v1beta1.tx_pb2'
        # @@protoc_insertion_point(class_scope:nibiru.oracle.v1beta1.MsgAggregateExchangeRateVote)
    },
)
_sym_db.RegisterMessage(MsgAggregateExchangeRateVote)

MsgAggregateExchangeRateVoteResponse = _reflection.GeneratedProtocolMessageType(
    'MsgAggregateExchangeRateVoteResponse',
    (_message.Message,),
    {
        'DESCRIPTOR': _MSGAGGREGATEEXCHANGERATEVOTERESPONSE,
        '__module__': 'oracle.v1beta1.tx_pb2'
        # @@protoc_insertion_point(class_scope:nibiru.oracle.v1beta1.MsgAggregateExchangeRateVoteResponse)
    },
)
_sym_db.RegisterMessage(MsgAggregateExchangeRateVoteResponse)

MsgDelegateFeedConsent = _reflection.GeneratedProtocolMessageType(
    'MsgDelegateFeedConsent',
    (_message.Message,),
    {
        'DESCRIPTOR': _MSGDELEGATEFEEDCONSENT,
        '__module__': 'oracle.v1beta1.tx_pb2'
        # @@protoc_insertion_point(class_scope:nibiru.oracle.v1beta1.MsgDelegateFeedConsent)
    },
)
_sym_db.RegisterMessage(MsgDelegateFeedConsent)

MsgDelegateFeedConsentResponse = _reflection.GeneratedProtocolMessageType(
    'MsgDelegateFeedConsentResponse',
    (_message.Message,),
    {
        'DESCRIPTOR': _MSGDELEGATEFEEDCONSENTRESPONSE,
        '__module__': 'oracle.v1beta1.tx_pb2'
        # @@protoc_insertion_point(class_scope:nibiru.oracle.v1beta1.MsgDelegateFeedConsentResponse)
    },
)
_sym_db.RegisterMessage(MsgDelegateFeedConsentResponse)

_MSG = DESCRIPTOR.services_by_name['Msg']
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z,github.com/NibiruChain/nibiru/x/oracle/types'
    _MSGAGGREGATEEXCHANGERATEPREVOTE.fields_by_name['hash']._options = None
    _MSGAGGREGATEEXCHANGERATEPREVOTE.fields_by_name['hash']._serialized_options = b'\362\336\037\013yaml:\"hash\"'
    _MSGAGGREGATEEXCHANGERATEPREVOTE.fields_by_name['feeder']._options = None
    _MSGAGGREGATEEXCHANGERATEPREVOTE.fields_by_name['feeder']._serialized_options = b'\362\336\037\ryaml:\"feeder\"'
    _MSGAGGREGATEEXCHANGERATEPREVOTE.fields_by_name['validator']._options = None
    _MSGAGGREGATEEXCHANGERATEPREVOTE.fields_by_name[
        'validator'
    ]._serialized_options = b'\362\336\037\020yaml:\"validator\"'
    _MSGAGGREGATEEXCHANGERATEPREVOTE._options = None
    _MSGAGGREGATEEXCHANGERATEPREVOTE._serialized_options = b'\350\240\037\000\210\240\037\000'
    _MSGAGGREGATEEXCHANGERATEVOTE.fields_by_name['salt']._options = None
    _MSGAGGREGATEEXCHANGERATEVOTE.fields_by_name['salt']._serialized_options = b'\362\336\037\013yaml:\"salt\"'
    _MSGAGGREGATEEXCHANGERATEVOTE.fields_by_name['exchange_rates']._options = None
    _MSGAGGREGATEEXCHANGERATEVOTE.fields_by_name[
        'exchange_rates'
    ]._serialized_options = b'\362\336\037\025yaml:\"exchange_rates\"'
    _MSGAGGREGATEEXCHANGERATEVOTE.fields_by_name['feeder']._options = None
    _MSGAGGREGATEEXCHANGERATEVOTE.fields_by_name['feeder']._serialized_options = b'\362\336\037\ryaml:\"feeder\"'
    _MSGAGGREGATEEXCHANGERATEVOTE.fields_by_name['validator']._options = None
    _MSGAGGREGATEEXCHANGERATEVOTE.fields_by_name[
        'validator'
    ]._serialized_options = b'\362\336\037\020yaml:\"validator\"'
    _MSGAGGREGATEEXCHANGERATEVOTE._options = None
    _MSGAGGREGATEEXCHANGERATEVOTE._serialized_options = b'\350\240\037\000\210\240\037\000'
    _MSGDELEGATEFEEDCONSENT.fields_by_name['operator']._options = None
    _MSGDELEGATEFEEDCONSENT.fields_by_name['operator']._serialized_options = b'\362\336\037\017yaml:\"operator\"'
    _MSGDELEGATEFEEDCONSENT.fields_by_name['delegate']._options = None
    _MSGDELEGATEFEEDCONSENT.fields_by_name['delegate']._serialized_options = b'\362\336\037\017yaml:\"delegate\"'
    _MSGDELEGATEFEEDCONSENT._options = None
    _MSGDELEGATEFEEDCONSENT._serialized_options = b'\350\240\037\000\210\240\037\000'
    _MSGAGGREGATEEXCHANGERATEPREVOTE._serialized_start = 73
    _MSGAGGREGATEEXCHANGERATEPREVOTE._serialized_end = 223
    _MSGAGGREGATEEXCHANGERATEPREVOTERESPONSE._serialized_start = 225
    _MSGAGGREGATEEXCHANGERATEPREVOTERESPONSE._serialized_end = 266
    _MSGAGGREGATEEXCHANGERATEVOTE._serialized_start = 269
    _MSGAGGREGATEEXCHANGERATEVOTE._serialized_end = 467
    _MSGAGGREGATEEXCHANGERATEVOTERESPONSE._serialized_start = 469
    _MSGAGGREGATEEXCHANGERATEVOTERESPONSE._serialized_end = 507
    _MSGDELEGATEFEEDCONSENT._serialized_start = 509
    _MSGDELEGATEFEEDCONSENT._serialized_end = 621
    _MSGDELEGATEFEEDCONSENTRESPONSE._serialized_start = 623
    _MSGDELEGATEFEEDCONSENTRESPONSE._serialized_end = 655
    _MSG._serialized_start = 658
    _MSG._serialized_end = 1085
# @@protoc_insertion_point(module_scope)