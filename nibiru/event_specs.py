from dataclasses import dataclass
from enum import Enum

import google.protobuf.message
from nibiru_proto.proto.dex.v1 import tx_pb2 as dex_events  # noqa
from nibiru_proto.proto.lockup.v1 import tx_pb2 as lockup_events  # noqa
from nibiru_proto.proto.perp.v1 import event_pb2 as perp_events
from nibiru_proto.proto.pricefeed import tx_pb2 as pricefeed_events
from nibiru_proto.proto.stablecoin import events_pb2 as stablecoin_events  # noqa
from nibiru_proto.proto.vpool.v1 import event_pb2 as vpool_events


class EventType(Enum):
    """
    The events enum type shows the type of events available to parse from the nibiruwebsocket object.
    """

    # Perp events
    PositionChangedEvent = perp_events.PositionChangedEvent
    PositionSettledEvent = perp_events.PositionSettledEvent
    PositionLiquidatedEvent = perp_events.PositionLiquidatedEvent
    FundingRateChangedEvent = perp_events.FundingRateChangedEvent

    # Vpool events
    ReserveSnapshotSavedEvent = vpool_events.ReserveSnapshotSavedEvent
    SwapQuoteForBaseEvent = vpool_events.SwapQuoteForBaseEvent
    SwapBaseForQuoteEvent = vpool_events.SwapBaseForQuoteEvent
    MarkPriceChanged = vpool_events.MarkPriceChanged

    # # Dex event
    # PoolJoinedEvent = dex_events.EventPoolJoined
    # PoolCreatedEvent = dex_events.EventPoolCreated
    # PoolExitedEvent = dex_events.EventPoolExited
    # AssetsSwappedEvent = dex_events.EventAssetsSwapped

    # Lockup event
    # LockEvent = lockup_events.EventLock
    # UnlockInitiatedEvent = lockup_events.EventUnlockInitiated
    # UnlockEvent = lockup_events.EventUnlock

    # Pricefeed events
    OracleUpdatePriceEvent = pricefeed_events.EventOracleUpdatePrice
    PairPriceUpdatedEvent = pricefeed_events.EventPairPriceUpdated

    # Stablecoin events
    # TransferEvent = stablecoin_events.EventTransfer
    # MintStableEvent = stablecoin_events.EventMintStable
    # BurnStableEvent = stablecoin_events.EventBurnStable
    # MintNIBIEvent = stablecoin_events.EventMintNIBI
    # BurnNIBIEvent = stablecoin_events.EventBurnNIBI
    # RecollateralizeEvent = stablecoin_events.EventRecollateralize
    # BuybackEvent = stablecoin_events.EventBuyback

    # Bank
    Transfer = "transfer"

    def get_full_path(self):
        if isinstance(self.value, str):
            return self.value
        proto_message: google.protobuf.message.Message = self.value
        return str(proto_message.DESCRIPTOR.full_name)


@dataclass
class EventCaptured:
    event_type: EventType
    payload: dict
