from dataclasses import dataclass
from enum import Enum

import google.protobuf.message
from nibiru_proto.proto.perp.v1 import event_pb2 as perp_events
from nibiru_proto.proto.spot.v1 import event_pb2 as spot_events
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
    SwapOnVpoolEvent = vpool_events.SwapOnVpoolEvent
    MarkPriceChanged = vpool_events.MarkPriceChangedEvent

    # Spot event
    PoolJoinedEvent = spot_events.EventPoolJoined
    PoolCreatedEvent = spot_events.EventPoolCreated
    PoolExitedEvent = spot_events.EventPoolExited
    AssetsSwappedEvent = spot_events.EventAssetsSwapped

    # Stablecoin events
    TransferEvent = stablecoin_events.EventTransfer
    MintStableEvent = stablecoin_events.EventMintStable
    BurnStableEvent = stablecoin_events.EventBurnStable
    MintNIBIEvent = stablecoin_events.EventMintNIBI
    BurnNIBIEvent = stablecoin_events.EventBurnNIBI
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
