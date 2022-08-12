"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import common.common_pb2
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _Direction:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _DirectionEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_Direction.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    DIRECTION_UNSPECIFIED: _Direction.ValueType  # 0
    ADD_TO_POOL: _Direction.ValueType  # 1
    REMOVE_FROM_POOL: _Direction.ValueType  # 2
class Direction(_Direction, metaclass=_DirectionEnumTypeWrapper):
    pass

DIRECTION_UNSPECIFIED: Direction.ValueType  # 0
ADD_TO_POOL: Direction.ValueType  # 1
REMOVE_FROM_POOL: Direction.ValueType  # 2
global___Direction = Direction


class _TwapCalcOption:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _TwapCalcOptionEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_TwapCalcOption.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    TWAP_CALC_OPTION_UNSPECIFIED: _TwapCalcOption.ValueType  # 0
    SPOT: _TwapCalcOption.ValueType  # 1
    """Spot price from quote asset reserve / base asset reserve"""

    QUOTE_ASSET_SWAP: _TwapCalcOption.ValueType  # 2
    """Swapping with quote assets, output denominated in base assets"""

    BASE_ASSET_SWAP: _TwapCalcOption.ValueType  # 3
    """Swapping with base assets, output denominated in quote assets"""

class TwapCalcOption(_TwapCalcOption, metaclass=_TwapCalcOptionEnumTypeWrapper):
    """Enumerates different options of calculating twap."""
    pass

TWAP_CALC_OPTION_UNSPECIFIED: TwapCalcOption.ValueType  # 0
SPOT: TwapCalcOption.ValueType  # 1
"""Spot price from quote asset reserve / base asset reserve"""

QUOTE_ASSET_SWAP: TwapCalcOption.ValueType  # 2
"""Swapping with quote assets, output denominated in base assets"""

BASE_ASSET_SWAP: TwapCalcOption.ValueType  # 3
"""Swapping with base assets, output denominated in quote assets"""

global___TwapCalcOption = TwapCalcOption


class ReserveSnapshot(google.protobuf.message.Message):
    """a snapshot of the vpool's reserves at a given point in time"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    BASE_ASSET_RESERVE_FIELD_NUMBER: builtins.int
    QUOTE_ASSET_RESERVE_FIELD_NUMBER: builtins.int
    TIMESTAMP_MS_FIELD_NUMBER: builtins.int
    BLOCK_NUMBER_FIELD_NUMBER: builtins.int
    base_asset_reserve: typing.Text
    quote_asset_reserve: typing.Text
    """quote asset is usually the margin asset, e.g. NUSD"""

    timestamp_ms: builtins.int
    """milliseconds since unix epoch"""

    block_number: builtins.int
    def __init__(self,
        *,
        base_asset_reserve: typing.Text = ...,
        quote_asset_reserve: typing.Text = ...,
        timestamp_ms: builtins.int = ...,
        block_number: builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["base_asset_reserve",b"base_asset_reserve","block_number",b"block_number","quote_asset_reserve",b"quote_asset_reserve","timestamp_ms",b"timestamp_ms"]) -> None: ...
global___ReserveSnapshot = ReserveSnapshot

class Pool(google.protobuf.message.Message):
    """A virtual pool used only for price discovery of perpetual futures contracts.
    No real liquidity exists in this pool.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PAIR_FIELD_NUMBER: builtins.int
    BASE_ASSET_RESERVE_FIELD_NUMBER: builtins.int
    QUOTE_ASSET_RESERVE_FIELD_NUMBER: builtins.int
    TRADE_LIMIT_RATIO_FIELD_NUMBER: builtins.int
    FLUCTUATION_LIMIT_RATIO_FIELD_NUMBER: builtins.int
    MAX_ORACLE_SPREAD_RATIO_FIELD_NUMBER: builtins.int
    MAINTENANCE_MARGIN_RATIO_FIELD_NUMBER: builtins.int
    MAX_LEVERAGE_FIELD_NUMBER: builtins.int
    @property
    def pair(self) -> common.common_pb2.AssetPair:
        """always BASE:QUOTE, e.g. BTC:NUSD or ETH:NUSD"""
        pass
    base_asset_reserve: typing.Text
    """base asset is the crypto asset, e.g. BTC or ETH"""

    quote_asset_reserve: typing.Text
    """quote asset is usually stablecoin, in our case NUSD"""

    trade_limit_ratio: typing.Text
    """ratio applied to reserves in order not to over trade"""

    fluctuation_limit_ratio: typing.Text
    """percentage that a single open or close position can alter the reserve amounts"""

    max_oracle_spread_ratio: typing.Text
    """max_oracle_spread_ratio"""

    maintenance_margin_ratio: typing.Text
    """maintenance_margin_ratio"""

    max_leverage: typing.Text
    """max_leverage"""

    def __init__(self,
        *,
        pair: typing.Optional[common.common_pb2.AssetPair] = ...,
        base_asset_reserve: typing.Text = ...,
        quote_asset_reserve: typing.Text = ...,
        trade_limit_ratio: typing.Text = ...,
        fluctuation_limit_ratio: typing.Text = ...,
        max_oracle_spread_ratio: typing.Text = ...,
        maintenance_margin_ratio: typing.Text = ...,
        max_leverage: typing.Text = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["pair",b"pair"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["base_asset_reserve",b"base_asset_reserve","fluctuation_limit_ratio",b"fluctuation_limit_ratio","maintenance_margin_ratio",b"maintenance_margin_ratio","max_leverage",b"max_leverage","max_oracle_spread_ratio",b"max_oracle_spread_ratio","pair",b"pair","quote_asset_reserve",b"quote_asset_reserve","trade_limit_ratio",b"trade_limit_ratio"]) -> None: ...
global___Pool = Pool

class PoolPrices(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MARK_PRICE_FIELD_NUMBER: builtins.int
    INDEX_PRICE_FIELD_NUMBER: builtins.int
    TWAP_MARK_FIELD_NUMBER: builtins.int
    SWAP_INVARIANT_FIELD_NUMBER: builtins.int
    BLOCK_NUMBER_FIELD_NUMBER: builtins.int
    mark_price: typing.Text
    """MarkPrice is the instantaneous price of the perp.
    Equivalent to quoteAssetReserve / baseAssetReserve.
    """

    index_price: typing.Text
    """IndexPrice is the price of the "underlying" for the perp"""

    twap_mark: typing.Text
    """TwapMark is the time-weighted average (mark) price."""

    swap_invariant: typing.Text
    """SwapInvariant is the product of the reserves, commonly referred to as "k"."""

    block_number: builtins.int
    """The block number corresponding to each price"""

    def __init__(self,
        *,
        mark_price: typing.Text = ...,
        index_price: typing.Text = ...,
        twap_mark: typing.Text = ...,
        swap_invariant: typing.Text = ...,
        block_number: builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["block_number",b"block_number","index_price",b"index_price","mark_price",b"mark_price","swap_invariant",b"swap_invariant","twap_mark",b"twap_mark"]) -> None: ...
global___PoolPrices = PoolPrices
