from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    """
    The events enum type shows the type of events available to parse from the nibiruwebsocket object.
    """

    # Perp events
    PositionChangedEvent = "nibiru.perp.v1.PositionChangedEvent"
    PositionLiquidatedEvent = "nibiru.perp.v1.PositionLiquidatedEvent"
    FundingRateChangedEvent = "nibiru.perp.v1.FundingRateChangedEvent"
    PositionSettledEvent = "nibiru.perp.v1.PositionSettledEvent"

    # Vpool events
    ReserveSnapshotSavedEvent = "nibiru.vpool.v1.ReserveSnapshotSavedEvent"
    SwapQuoteForBaseEvent = "nibiru.vpool.v1.SwapQuoteForBaseEvent"
    MarkPriceChanged = "nibiru.vpool.v1.MarkPriceChanged"

    # Bank
    Transfer = "transfer"


@dataclass
class EventCaptured:
    event_type: EventType
    payload: dict
