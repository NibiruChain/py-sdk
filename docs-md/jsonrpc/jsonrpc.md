Module pysdk.jsonrpc.jsonrpc
============================

Functions
---------


`do_jsonrpc_request(data: Union[pysdk.jsonrpc.jsonrpc.JsonRPCRequest, pysdk.jsonrpc.jsonrpc.RawJsonRPCRequest], endpoint: str = 'http://localhost:26657', headers: Dict[str, str] = {'Content-Type': 'application/json'}) ‑> pysdk.jsonrpc.jsonrpc.JsonRPCResponse`
:


`do_jsonrpc_request_raw(data: Union[pysdk.jsonrpc.jsonrpc.JsonRPCRequest, pysdk.jsonrpc.jsonrpc.RawJsonRPCRequest], endpoint: str = 'http://localhost:26657', headers: Dict[str, str] = {'Content-Type': 'application/json'}) ‑> pysdk.jsonrpc.jsonrpc.RawJsonRPCResponse`
:


`json_rpc_request_keys() ‑> Set[str]`
:   Fields for a JSONRPCRequest. Must be one of:
    ["method", "params", "jsonrpc", "id"]


`json_rpc_response_keys() ‑> Set[str]`
:   Fields for a JSONRPCResponse. Must be one of:
    ["result", "error", "jsonrpc", "id"]

Classes
-------

`JsonRPCRequest(method: str, params: pysdk.pytypes.jsonable.Jsonable = None, jsonrpc: str = '2.0', id: Union[str, int, None] = None)`
:   JsonRPCRequest(method: str, params: pysdk.pytypes.jsonable.Jsonable = None, jsonrpc: str = '2.0', id: Union[str, int, NoneType] = None)

    ### Descendants

    * pysdk.tmrpc.broadcast.BroadcastTxSync
    * pysdk.tmrpc.broadcast.TypedJsonRpcRequest

    ### Class variables

    `id: Union[str, int, None]`
    :

    `jsonrpc: str`
    :

    `method: str`
    :

    `params: pysdk.pytypes.jsonable.Jsonable`
    :

    ### Static methods

    `from_raw_dict(raw: RawJsonRPCRequest) ‑> pysdk.jsonrpc.jsonrpc.JsonRPCRequest`
    :

    ### Methods

    `to_dict(self) ‑> Dict[str, Any]`
    :

`JsonRPCResponse(id: Union[str, int, None] = None, jsonrpc: str = '2.0', result: Any = None, error: Any = None)`
:   Generic JSON-RPC response as dictated by the official
    [JSON-RPC 2.0 specification](https://www.jsonrpc.org/specification).

    Args and Attributes:
        id (JsonRPCID):
        jsonrpc (str = "2.0"):
        result (TODO, optional): Defaults to None.
        error (TODO, optional): Defaults to None.

    ### Class variables

    `error: Any`
    :

    `id: Union[str, int, None]`
    :

    `jsonrpc: str`
    :

    `result: Any`
    :

    ### Static methods

    `from_raw_dict(raw: RawJsonRPCResponse) ‑> pysdk.jsonrpc.jsonrpc.JsonRPCResponse`
    :

    ### Methods

    `ok(self) ‑> bool`
    :

    `to_dict(self) ‑> pysdk.jsonrpc.jsonrpc.RawJsonRPCResponse`
    :

`RawJsonRPCRequest(*args, **kwargs)`
:   Proxy for a 'TypedDict' representing a JSON RPC response.

    The 'JsonRPCRequest' type is defined according to the official
    [JSON-RPC 2.0 specification](https://www.jsonrpc.org/specification).

    Keys (ValueType):
        method (str): A string containing the name of the method to be invoked.
          Method names that begin with the word rpc followed by a period
          character (U+002E or ASCII 46) are reserved for rpc-internal methods
          and extensions and MUST NOT be used for anything else.
        params (TODO): A structured value that holds the parameter values to be
            used during the invocation of the method. This field MAY be omitted.

        jsonrpc (str): Specifies the version of the JSON-RPC protocol.
            MUST be exactly "2.0".

        id (str): An identifier established by the Client that MUST contain a
          String, Number, or NULL value if included. If it is not included, it
          is assumed to be a notification.
          1. The value SHOULD normally not be Null: The use of Null as a value
             for the id member in a Request object is discouraged, because this
             specification uses a value of Null for Responses with an unknown
             id. Also, because JSON-RPC 1.0 uses an id value of Null for
             Notifications this could cause confusion in handling.
          2. The Numbers in the id SHOULD NOT contain fractional parts:
             Fractional parts may be problematic, since many decimal fractions
             cannot be represented exactly as binary fractions.

    Note that the Server MUST reply with the same value in the Response object
    if included. This member is used to correlate the context between the two
    objects.

    ### Ancestors (in MRO)

    * builtins.dict

`RawJsonRPCResponse(*args, **kwargs)`
:   Proxy for a 'TypedDict' representing a JSON RPC response.

    The 'JsonRPCResponse' type is defined according to the official
    [JSON-RPC 2.0 specification](https://www.jsonrpc.org/specification).

    Keys (ValueType):
        result (TODO): ...
        error (TODO): ...
        jsonrpc (str): Should be "2.0".
        id (str): block height at which the transaction was committed.

    ### Ancestors (in MRO)

    * builtins.dict
