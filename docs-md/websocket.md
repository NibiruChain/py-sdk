Module nibiru.websocket
=======================

Classes
-------

`NibiruWebsocket(network: nibiru.network.Network, captured_events_type: List[nibiru.event_specs.EventType] = [], tx_fail_queue: <bound method BaseContext.Queue of <multiprocessing.context.DefaultContext object at 0x7f5ead984410>> = None)`
:   The nibiru listener provides an interface to easily connect and handle subscription to the events of a nibiru
    chain.

    ### Class variables

    `captured_events_type: List[List[str]]`
    :

    `queue: <bound method BaseContext.Queue of <multiprocessing.context.DefaultContext object at 0x7f5ead984410>>`
    :

    `tx_fail_queue: <bound method BaseContext.Queue of <multiprocessing.context.DefaultContext object at 0x7f5ead984410>>`
    :

    ### Methods

    `start(self)`
    :   Start the websocket and fill the queue with events.
