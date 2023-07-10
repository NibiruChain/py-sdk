Module pysdk.event_specs
========================

Classes
-------

`EventCaptured(event_type: pysdk.event_specs.EventType, payload: dict)`
:   EventCaptured(event_type: pysdk.event_specs.EventType, payload: dict)

    ### Class variables

    `event_type: pysdk.event_specs.EventType`
    :

    `payload: dict`
    :

`EventType(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   The events enum type shows the type of events available to parse from the nibiruwebsocket object.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `AssetsSwappedEvent`
    :

    `BurnNIBIEvent`
    :

    `BurnStableEvent`
    :

    `BuybackEvent`
    :

    `Delegate`
    :

    `EventAggregatePrevote`
    :

    `EventAggregateVote`
    :

    `EventDelegateFeederConsent`
    :

    `FundingRateChangedEvent`
    :

    `MintNIBIEvent`
    :

    `MintStableEvent`
    :

    `PoolCreatedEvent`
    :

    `PoolExitedEvent`
    :

    `PoolJoinedEvent`
    :

    `PositionChangedEvent`
    :

    `PositionLiquidatedEvent`
    :

    `PositionSettledEvent`
    :

    `PriceUpdate`
    :

    `RecollateralizeEvent`
    :

    `Redelegate`
    :

    `Transfer`
    :

    `TransferEvent`
    :

    `Unbond`
    :

    ### Methods

    `get_full_path(self)`
    :
