Module pysdk.websocket
======================

Classes
-------

`NibiruWebsocket(network: pysdk.pytypes.network.Network, captured_event_types: List[pysdk.event_specs.EventType] = <factory>, queue: <bound method BaseContext.Queue of <multiprocessing.context.DefaultContext object at 0x7f49907cc4c0>> = <multiprocessing.queues.Queue object>, tx_fail_queue: <bound method BaseContext.Queue of <multiprocessing.context.DefaultContext object at 0x7f49907cc4c0>> = <multiprocessing.queues.Queue object>, captured_event_types_map: Dict[str, pysdk.event_specs.EventType] = <factory>, logger: logging.Logger = <Logger ws-logger (WARNING)>)`
:   NibiruWebsocket(network: pysdk.pytypes.network.Network, captured_event_types: List[pysdk.event_specs.EventType] = <factory>, queue: <bound method BaseContext.Queue of <multiprocessing.context.DefaultContext object at 0x7f49907cc4c0>> = <multiprocessing.queues.Queue object at 0x7f49908a3f70>, tx_fail_queue: <bound method BaseContext.Queue of <multiprocessing.context.DefaultContext object at 0x7f49907cc4c0>> = <multiprocessing.queues.Queue object at 0x7f499076c460>, captured_event_types_map: Dict[str, pysdk.event_specs.EventType] = <factory>, logger: logging.Logger = <Logger ws-logger (WARNING)>)

    ### Class variables

    `captured_event_types: List[pysdk.event_specs.EventType]`
    :

    `captured_event_types_map: Dict[str, pysdk.event_specs.EventType]`
    :

    `logger: logging.Logger`
    :

    `network: pysdk.pytypes.network.Network`
    :

    `queue: <bound method BaseContext.Queue of <multiprocessing.context.DefaultContext object at 0x7f49907cc4c0>>`
    :

    `tx_fail_queue: <bound method BaseContext.Queue of <multiprocessing.context.DefaultContext object at 0x7f49907cc4c0>>`
    :

    ### Methods

    `start(self)`
    :   Start the websocket and fill the queue with events.
