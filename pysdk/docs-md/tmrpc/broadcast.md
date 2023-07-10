Module pysdk.tmrpc.broadcast
============================

Functions
---------


`is_known_rpc_method(method: str) ‑> Tuple[bool, Optional[Callable]]`
:

Classes
-------

`BroadcastTxSync(method: str, params: pysdk.pytypes.jsonable.Jsonable = None, jsonrpc: str = '2.0', id: Union[str, int, None] = None)`
:   TODO docs

    Args:
        req (Union[jsonrpc.JsonRPCRequest, str, dict]): An object that can be
            parsed as a jsonrpc.JsonRPCRequest.

    ### Ancestors (in MRO)

    * pysdk.jsonrpc.jsonrpc.JsonRPCRequest

    ### Class variables

    `id: Union[str, int, None]`
    :

    `jsonrpc: str`
    :

    `method: str`
    :

    `params: pysdk.pytypes.jsonable.Jsonable`
    :

    ### Methods

    `create(tx_raw_bytes: Union[bytes, str], id=None) ‑> pysdk.jsonrpc.jsonrpc.JsonRPCRequest`
    :

`TypedJsonRpcRequest(method: str, params: pysdk.pytypes.jsonable.Jsonable = None, jsonrpc: str = '2.0', id: Union[str, int, None] = None)`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * abc.ABC
    * pysdk.jsonrpc.jsonrpc.JsonRPCRequest

    ### Class variables

    `id: Union[str, int, None]`
    :

    `jsonrpc: str`
    :

    `method: str`
    :

    `params: pysdk.pytypes.jsonable.Jsonable`
    :

    ### Methods

    `create(cls, *args) ‑> pysdk.jsonrpc.jsonrpc.JsonRPCRequest`
    :   TODO docs
