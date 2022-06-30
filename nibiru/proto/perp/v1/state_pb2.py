# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: perp/v1/state.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
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
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13perp/v1/state.proto\x12\x0enibiru.perp.v1\x1a\x14gogoproto/gogo.proto\x1a\x1e\x63osmos/base/v1beta1/coin.proto\x1a\x19\x63osmos_proto/cosmos.proto\x1a\x1egoogle/protobuf/duration.proto\"\xca\x04\n\x06Params\x12\x0f\n\x07stopped\x18\x01 \x01(\x08\x12P\n\x18maintenance_margin_ratio\x18\x02 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12J\n\x12\x66\x65\x65_pool_fee_ratio\x18\x03 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12P\n\x18\x65\x63osystem_fund_fee_ratio\x18\x04 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12M\n\x15liquidation_fee_ratio\x18\x05 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12Q\n\x19partial_liquidation_ratio\x18\x06 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12\x18\n\x10\x65poch_identifier\x18\x07 \x01(\t\x12\x82\x01\n\x14twap_lookback_window\x18\x08 \x01(\x0b\x32\x19.google.protobuf.DurationBI\xc8\xde\x1f\x00\x98\xdf\x1f\x01\xea\xde\x1f\x1etwap_lookback_window,omitempty\xf2\xde\x1f\x1byaml:\"twap_lookback_window\"\"\x88\x04\n\x0cGenesisState\x12,\n\x06params\x18\x01 \x01(\x0b\x32\x16.nibiru.perp.v1.ParamsB\x04\xc8\xde\x1f\x00\x12W\n\rvault_balance\x18\x02 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB%\xf2\xde\x1f\x1dyaml:\"module_account_balance\"\xc8\xde\x1f\x00\x12Y\n\x0fperp_ef_balance\x18\x03 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB%\xf2\xde\x1f\x1dyaml:\"module_account_balance\"\xc8\xde\x1f\x00\x12Z\n\x10\x66\x65\x65_pool_balance\x18\x04 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB%\xf2\xde\x1f\x1dyaml:\"module_account_balance\"\xc8\xde\x1f\x00\x12\x33\n\rpair_metadata\x18\x05 \x03(\x0b\x32\x1c.nibiru.perp.v1.PairMetadata\x12+\n\tpositions\x18\x06 \x03(\x0b\x32\x18.nibiru.perp.v1.Position\x12\x39\n\x11prepaid_bad_debts\x18\x07 \x03(\x0b\x32\x1e.nibiru.perp.v1.PrepaidBadDebt\x12\x1d\n\x15whitelisted_addresses\x18\x08 \x03(\t\"\xec\x02\n\x08Position\x12\x16\n\x0etrader_address\x18\x01 \x01(\t\x12\x0c\n\x04pair\x18\x02 \x01(\t\x12<\n\x04size\x18\x03 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12>\n\x06margin\x18\x04 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12\x45\n\ropen_notional\x18\x05 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12_\n\'last_update_cumulative_premium_fraction\x18\x06 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12\x14\n\x0c\x62lock_number\x18\x07 \x01(\x03\"\x90\x05\n\x0cPositionResp\x12*\n\x08position\x18\x01 \x01(\x0b\x32\x18.nibiru.perp.v1.Position\x12P\n\x18\x65xchanged_notional_value\x18\x02 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12O\n\x17\x65xchanged_position_size\x18\x03 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12@\n\x08\x62\x61\x64_debt\x18\x04 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12G\n\x0f\x66unding_payment\x18\x05 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12\x44\n\x0crealized_pnl\x18\x06 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12L\n\x14unrealized_pnl_after\x18\x07 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12G\n\x0fmargin_to_vault\x18\x08 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12I\n\x11position_notional\x18\t \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\"\xb9\x02\n\rLiquidateResp\x12@\n\x08\x62\x61\x64_debt\x18\x01 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12I\n\x11\x66\x65\x65_to_liquidator\x18\x02 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00\x12R\n\x1a\x66\x65\x65_to_perp_ecosystem_fund\x18\x03 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00\x12\x12\n\nliquidator\x18\x04 \x01(\t\x12\x33\n\rposition_resp\x18\x05 \x01(\x0b\x32\x1c.nibiru.perp.v1.PositionResp\"r\n\x0cPairMetadata\x12\x0c\n\x04pair\x18\x01 \x01(\t\x12T\n\x1c\x63umulative_premium_fractions\x18\x02 \x03(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\"_\n\x0ePrepaidBadDebt\x12\r\n\x05\x64\x65nom\x18\x01 \x01(\t\x12>\n\x06\x61mount\x18\x02 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00*/\n\x04Side\x12\x14\n\x10SIDE_UNSPECIFIED\x10\x00\x12\x07\n\x03\x42UY\x10\x01\x12\x08\n\x04SELL\x10\x02*V\n\rPnLCalcOption\x12\x1f\n\x1bPNL_CALC_OPTION_UNSPECIFIED\x10\x00\x12\x0e\n\nSPOT_PRICE\x10\x01\x12\x08\n\x04TWAP\x10\x02\x12\n\n\x06ORACLE\x10\x03*G\n\x13PnLPreferenceOption\x12\x1e\n\x1aPNL_PREFERENCE_UNSPECIFIED\x10\x00\x12\x07\n\x03MAX\x10\x01\x12\x07\n\x03MIN\x10\x02*q\n\x1cMarginCalculationPriceOption\x12/\n+MARGIN_CALCULATION_PRICE_OPTION_UNSPECIFIED\x10\x00\x12\x08\n\x04SPOT\x10\x01\x12\t\n\x05INDEX\x10\x02\x12\x0b\n\x07MAX_PNL\x10\x03\x42,Z*github.com/NibiruChain/nibiru/x/perp/typesb\x06proto3')

_SIDE = DESCRIPTOR.enum_types_by_name['Side']
Side = enum_type_wrapper.EnumTypeWrapper(_SIDE)
_PNLCALCOPTION = DESCRIPTOR.enum_types_by_name['PnLCalcOption']
PnLCalcOption = enum_type_wrapper.EnumTypeWrapper(_PNLCALCOPTION)
_PNLPREFERENCEOPTION = DESCRIPTOR.enum_types_by_name['PnLPreferenceOption']
PnLPreferenceOption = enum_type_wrapper.EnumTypeWrapper(_PNLPREFERENCEOPTION)
_MARGINCALCULATIONPRICEOPTION = DESCRIPTOR.enum_types_by_name['MarginCalculationPriceOption']
MarginCalculationPriceOption = enum_type_wrapper.EnumTypeWrapper(_MARGINCALCULATIONPRICEOPTION)
SIDE_UNSPECIFIED = 0
BUY = 1
SELL = 2
PNL_CALC_OPTION_UNSPECIFIED = 0
SPOT_PRICE = 1
TWAP = 2
ORACLE = 3
PNL_PREFERENCE_UNSPECIFIED = 0
MAX = 1
MIN = 2
MARGIN_CALCULATION_PRICE_OPTION_UNSPECIFIED = 0
SPOT = 1
INDEX = 2
MAX_PNL = 3


_PARAMS = DESCRIPTOR.message_types_by_name['Params']
_GENESISSTATE = DESCRIPTOR.message_types_by_name['GenesisState']
_POSITION = DESCRIPTOR.message_types_by_name['Position']
_POSITIONRESP = DESCRIPTOR.message_types_by_name['PositionResp']
_LIQUIDATERESP = DESCRIPTOR.message_types_by_name['LiquidateResp']
_PAIRMETADATA = DESCRIPTOR.message_types_by_name['PairMetadata']
_PREPAIDBADDEBT = DESCRIPTOR.message_types_by_name['PrepaidBadDebt']
Params = _reflection.GeneratedProtocolMessageType('Params', (_message.Message,), {
  'DESCRIPTOR' : _PARAMS,
  '__module__' : 'perp.v1.state_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.perp.v1.Params)
  })
_sym_db.RegisterMessage(Params)

GenesisState = _reflection.GeneratedProtocolMessageType('GenesisState', (_message.Message,), {
  'DESCRIPTOR' : _GENESISSTATE,
  '__module__' : 'perp.v1.state_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.perp.v1.GenesisState)
  })
_sym_db.RegisterMessage(GenesisState)

Position = _reflection.GeneratedProtocolMessageType('Position', (_message.Message,), {
  'DESCRIPTOR' : _POSITION,
  '__module__' : 'perp.v1.state_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.perp.v1.Position)
  })
_sym_db.RegisterMessage(Position)

PositionResp = _reflection.GeneratedProtocolMessageType('PositionResp', (_message.Message,), {
  'DESCRIPTOR' : _POSITIONRESP,
  '__module__' : 'perp.v1.state_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.perp.v1.PositionResp)
  })
_sym_db.RegisterMessage(PositionResp)

LiquidateResp = _reflection.GeneratedProtocolMessageType('LiquidateResp', (_message.Message,), {
  'DESCRIPTOR' : _LIQUIDATERESP,
  '__module__' : 'perp.v1.state_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.perp.v1.LiquidateResp)
  })
_sym_db.RegisterMessage(LiquidateResp)

PairMetadata = _reflection.GeneratedProtocolMessageType('PairMetadata', (_message.Message,), {
  'DESCRIPTOR' : _PAIRMETADATA,
  '__module__' : 'perp.v1.state_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.perp.v1.PairMetadata)
  })
_sym_db.RegisterMessage(PairMetadata)

PrepaidBadDebt = _reflection.GeneratedProtocolMessageType('PrepaidBadDebt', (_message.Message,), {
  'DESCRIPTOR' : _PREPAIDBADDEBT,
  '__module__' : 'perp.v1.state_pb2'
  # @@protoc_insertion_point(class_scope:nibiru.perp.v1.PrepaidBadDebt)
  })
_sym_db.RegisterMessage(PrepaidBadDebt)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z*github.com/NibiruChain/nibiru/x/perp/types'
  _PARAMS.fields_by_name['maintenance_margin_ratio']._options = None
  _PARAMS.fields_by_name['maintenance_margin_ratio']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _PARAMS.fields_by_name['fee_pool_fee_ratio']._options = None
  _PARAMS.fields_by_name['fee_pool_fee_ratio']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _PARAMS.fields_by_name['ecosystem_fund_fee_ratio']._options = None
  _PARAMS.fields_by_name['ecosystem_fund_fee_ratio']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _PARAMS.fields_by_name['liquidation_fee_ratio']._options = None
  _PARAMS.fields_by_name['liquidation_fee_ratio']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _PARAMS.fields_by_name['partial_liquidation_ratio']._options = None
  _PARAMS.fields_by_name['partial_liquidation_ratio']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _PARAMS.fields_by_name['twap_lookback_window']._options = None
  _PARAMS.fields_by_name['twap_lookback_window']._serialized_options = b'\310\336\037\000\230\337\037\001\352\336\037\036twap_lookback_window,omitempty\362\336\037\033yaml:\"twap_lookback_window\"'
  _GENESISSTATE.fields_by_name['params']._options = None
  _GENESISSTATE.fields_by_name['params']._serialized_options = b'\310\336\037\000'
  _GENESISSTATE.fields_by_name['vault_balance']._options = None
  _GENESISSTATE.fields_by_name['vault_balance']._serialized_options = b'\362\336\037\035yaml:\"module_account_balance\"\310\336\037\000'
  _GENESISSTATE.fields_by_name['perp_ef_balance']._options = None
  _GENESISSTATE.fields_by_name['perp_ef_balance']._serialized_options = b'\362\336\037\035yaml:\"module_account_balance\"\310\336\037\000'
  _GENESISSTATE.fields_by_name['fee_pool_balance']._options = None
  _GENESISSTATE.fields_by_name['fee_pool_balance']._serialized_options = b'\362\336\037\035yaml:\"module_account_balance\"\310\336\037\000'
  _POSITION.fields_by_name['size']._options = None
  _POSITION.fields_by_name['size']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _POSITION.fields_by_name['margin']._options = None
  _POSITION.fields_by_name['margin']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _POSITION.fields_by_name['open_notional']._options = None
  _POSITION.fields_by_name['open_notional']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _POSITION.fields_by_name['last_update_cumulative_premium_fraction']._options = None
  _POSITION.fields_by_name['last_update_cumulative_premium_fraction']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _POSITIONRESP.fields_by_name['exchanged_notional_value']._options = None
  _POSITIONRESP.fields_by_name['exchanged_notional_value']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _POSITIONRESP.fields_by_name['exchanged_position_size']._options = None
  _POSITIONRESP.fields_by_name['exchanged_position_size']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _POSITIONRESP.fields_by_name['bad_debt']._options = None
  _POSITIONRESP.fields_by_name['bad_debt']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _POSITIONRESP.fields_by_name['funding_payment']._options = None
  _POSITIONRESP.fields_by_name['funding_payment']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _POSITIONRESP.fields_by_name['realized_pnl']._options = None
  _POSITIONRESP.fields_by_name['realized_pnl']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _POSITIONRESP.fields_by_name['unrealized_pnl_after']._options = None
  _POSITIONRESP.fields_by_name['unrealized_pnl_after']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _POSITIONRESP.fields_by_name['margin_to_vault']._options = None
  _POSITIONRESP.fields_by_name['margin_to_vault']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _POSITIONRESP.fields_by_name['position_notional']._options = None
  _POSITIONRESP.fields_by_name['position_notional']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _LIQUIDATERESP.fields_by_name['bad_debt']._options = None
  _LIQUIDATERESP.fields_by_name['bad_debt']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _LIQUIDATERESP.fields_by_name['fee_to_liquidator']._options = None
  _LIQUIDATERESP.fields_by_name['fee_to_liquidator']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Int\310\336\037\000'
  _LIQUIDATERESP.fields_by_name['fee_to_perp_ecosystem_fund']._options = None
  _LIQUIDATERESP.fields_by_name['fee_to_perp_ecosystem_fund']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Int\310\336\037\000'
  _PAIRMETADATA.fields_by_name['cumulative_premium_fractions']._options = None
  _PAIRMETADATA.fields_by_name['cumulative_premium_fractions']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000'
  _PREPAIDBADDEBT.fields_by_name['amount']._options = None
  _PREPAIDBADDEBT.fields_by_name['amount']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Int\310\336\037\000'
  _SIDE._serialized_start=2819
  _SIDE._serialized_end=2866
  _PNLCALCOPTION._serialized_start=2868
  _PNLCALCOPTION._serialized_end=2954
  _PNLPREFERENCEOPTION._serialized_start=2956
  _PNLPREFERENCEOPTION._serialized_end=3027
  _MARGINCALCULATIONPRICEOPTION._serialized_start=3029
  _MARGINCALCULATIONPRICEOPTION._serialized_end=3142
  _PARAMS._serialized_start=153
  _PARAMS._serialized_end=739
  _GENESISSTATE._serialized_start=742
  _GENESISSTATE._serialized_end=1262
  _POSITION._serialized_start=1265
  _POSITION._serialized_end=1629
  _POSITIONRESP._serialized_start=1632
  _POSITIONRESP._serialized_end=2288
  _LIQUIDATERESP._serialized_start=2291
  _LIQUIDATERESP._serialized_end=2604
  _PAIRMETADATA._serialized_start=2606
  _PAIRMETADATA._serialized_end=2720
  _PREPAIDBADDEBT._serialized_start=2722
  _PREPAIDBADDEBT._serialized_end=2817
# @@protoc_insertion_point(module_scope)
