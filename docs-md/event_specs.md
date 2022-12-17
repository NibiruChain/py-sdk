Module nibiru.event_specs
=========================

Classes
-------

`EventCaptured(event_type: nibiru.event_specs.EventType, payload: dict)`
:   EventCaptured(event_type: nibiru.event_specs.EventType, payload: dict)

    ### Class variables

    `event_type: nibiru.event_specs.EventType`
    :

    `payload: dict`
    :

`EventType(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   The events enum type shows the type of events available to parse from the nibiruwebsocket object.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `Delegate`
    :

    `FundingRateChangedEvent`
    :

    `MarkPriceChanged`
    :

    `OracleUpdatePriceEvent`
    :

    `PairPriceUpdatedEvent`
    :

    `PositionChangedEvent`
    :

    `PositionLiquidatedEvent`
    :

    `PositionSettledEvent`
    :

    `Redelegate`
    :

    `ReserveSnapshotSavedEvent`
    :

    `SwapOnVpoolEvent`
    :

    `Transfer`
    :

    `Unbond`
    :

    ### Methods

    `get_full_path(self)`
    :
