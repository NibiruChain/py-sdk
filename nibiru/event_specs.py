from dataclasses import dataclass
from enum import Enum

import google.protobuf.message
import nibiru_proto.nibiru.dex.v1 as dex_events  # noqa
import nibiru_proto.nibiru.lockup.v1 as lockup_events  # noqa
import nibiru_proto.nibiru.perp.v1 as perp_events
import nibiru_proto.nibiru.stablecoin.v1 as stablecoin_events  # noqa
import nibiru_proto.nibiru.vpool.v1 as vpool_events


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
    SwapOnVpoolEvent = vpool_events.SwapOnVpoolEvent
    MarkPriceChanged = vpool_events.MarkPriceChangedEvent

    # Dex event
    PoolJoinedEvent = dex_events.EventPoolJoined
    PoolCreatedEvent = dex_events.EventPoolCreated
    PoolExitedEvent = dex_events.EventPoolExited
    AssetsSwappedEvent = dex_events.EventAssetsSwapped

    # Lockup event
    # LockEvent = lockup_events.EventLock
    # UnlockInitiatedEvent = lockup_events.EventUnlockInitiated
    # UnlockEvent = lockup_events.EventUnlock

    # Stablecoin events
    TransferEvent = stablecoin_events.EventTransfer
    MintStableEvent = stablecoin_events.EventMintStable
    BurnStableEvent = stablecoin_events.EventBurnStable
    MintNIBIEvent = stablecoin_events.EventMintNibi
    BurnNIBIEvent = stablecoin_events.EventBurnNibi
    RecollateralizeEvent = stablecoin_events.EventRecollateralize
    BuybackEvent = stablecoin_events.EventBuyback

    # Bank
    Transfer = "transfer"

    # Staking
    Delegate = "delegate"
    Unbond = "unbond"
    Redelegate = "redelegate"

    def get_full_path(self):
        if isinstance(self.value, str):
            return self.value
        proto_message: google.protobuf.message.Message = self.value
        return str(proto_message.DESCRIPTOR.full_name)


@dataclass
class EventCaptured:
    event_type: EventType
    payload: dict
