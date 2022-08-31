from dataclasses import dataclass
from enum import Enum


class Events(Enum):
    """
    The events enum type shows the type of events available to parse from the nibiruwebsocket object.
    """

    MarkPriceChanged = "nibiru.vpool.v1.MarkPriceChanged"
    PositionChangedEvent = "nibiru.perp.v1.PositionChangedEvent"


@dataclass
class EventCaptured:
    event_type: Events
    payload: dict
