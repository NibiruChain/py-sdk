import dataclasses
from typing import Any, Dict, Optional, Set, Union

import requests

from pysdk import pytypes
from pysdk.jsonrpc import rpc_error


def json_rpc_request_keys() -> Set[str]:
    """Fields for a JSONRPCRequest. Must be one of:
    ["method", "params", "jsonrpc", "id"]
    """
    return set(["method", "params", "jsonrpc", "id"])


def json_rpc_response_keys() -> Set[str]:
    """Fields for a JSONRPCResponse. Must be one of:
    ["result", "error", "jsonrpc", "id"]
    """
    return set(["result", "error", "jsonrpc", "id"])


JsonRPCID = Union[str, int]


@dataclasses.dataclass
class JsonRPCRequest:
    method: str
    params: pytypes.Jsonable = None
    jsonrpc: str = "2.0"
    id: Optional[JsonRPCID] = None

    def __post_init__(self):
        self._validate_method(method=self.method)
        self._validate_id(id=self.id)

    @staticmethod
    def _validate_method(method: str):
        if not isinstance(method, str):
            raise ValueError("Method must be a string.")
        if method.startswith("rpc."):
            raise ValueError("Method names beginning with 'rpc.' are reserved.")

    @staticmethod
    def _validate_id(id: Optional[Union[str, int]]):
        id_ = id
        if id_ is not None and not isinstance(id_, (str, int, type(None))):
            raise ValueError("id must be a string, number, or None.")
        if isinstance(id_, int) and id_ != int(id_):
            raise ValueError("id as number should not contain fractional parts.")

    def to_dict(self) -> Dict[str, Any]:
        request = {"jsonrpc": self.jsonrpc, "method": self.method}
        if self.params is not None:
            request["params"] = self.params
        if self.id is not None:
            request["id"] = self.id
        return request

    @classmethod
    def from_raw_dict(cls, raw: "RawJsonRPCRequest") -> "JsonRPCRequest":
        # Make sure the raw data is a dictionary
        if not isinstance(raw, dict):
            raise TypeError(f"Expected dict, got {type(raw)}")

        # Check for the required fields
        for field in ['jsonrpc', 'method']:
            if field not in raw and field != "jsonrpc":
                raise ValueError(f"Missing required field {field}")
            elif field == "jsonrpc":
                raw["jsonrpc"] = cls.jsonrpc

        # Create a JsonRPCRequest object from the raw dictionary
        jsonrpc = raw.get('jsonrpc')
        method = raw.get('method')
        params = raw.get('params', None)
        id = raw.get('id', None)
        return cls(method=method, params=params, id=id, jsonrpc=jsonrpc)


# from typing import TypedDict  # not available in Python 3.7
# class RawJsonRPCRequest(TypedDict):
class RawJsonRPCRequest(dict):
    """Proxy for a 'TypedDict' representing a JSON RPC response.

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
    """


# from typing import TypedDict  # not available in Python 3.7
# class RawJsonRPCResponse(TypedDict):
class RawJsonRPCResponse(dict):
    """Proxy for a 'TypedDict' representing a JSON RPC response.

    The 'JsonRPCResponse' type is defined according to the official
    [JSON-RPC 2.0 specification](https://www.jsonrpc.org/specification).

    Keys (ValueType):
        result (TODO): ...
        error (TODO): ...
        jsonrpc (str): Should be "2.0".
        id (str): block height at which the transaction was committed.
    """


@dataclasses.dataclass
class JsonRPCResponse:
    """Generic JSON-RPC response as dictated by the official
    [JSON-RPC 2.0 specification](https://www.jsonrpc.org/specification).

    Args and Attributes:
        id (JsonRPCID):
        jsonrpc (str = "2.0"):
        result (TODO, optional): Defaults to None.
        error (TODO, optional): Defaults to None.
    """

    id: Optional[JsonRPCID] = None
    jsonrpc: str = "2.0"
    result: Any = None
    error: Any = None

    def __post_init__(self):
        self._validate(result=self.result, error=self.error)

    def _validate(self, result, error):
        if result is not None and error is not None:
            raise ValueError("Both result and error cannot be set.")
        elif result is None and error is None:
            raise ValueError("Either result or error must be set.")
        elif result is not None:
            self.result = result
            self.error = None
        elif error is not None:
            if not isinstance(error, rpc_error.RPCError):
                raise ValueError("Error must be an instance of RPCError.")
            self.error = error.to_dict()
            self.result = None

    def to_dict(self) -> RawJsonRPCResponse:
        response: dict = {"jsonrpc": self.jsonrpc, "id": self.id}
        if self.result is not None:
            response["result"] = self.result
        if self.error is not None:
            response["error"] = self.error
        return response

    @classmethod
    def from_raw_dict(cls, raw: "RawJsonRPCResponse") -> "JsonRPCResponse":
        # Make sure the raw data is a dictionary
        if not isinstance(raw, dict):
            raise TypeError(f"Expected dict, got {type(raw)}")

        # Check for the required fields
        for field in ['jsonrpc', 'id']:
            if field not in raw:
                raise ValueError(f"Missing required field {field}")

        # Create a JsonRPCResponse object from the raw dictionary
        jsonrpc = raw.get('jsonrpc')
        id = raw.get('id')
        result = raw.get('result', None)
        error = raw.get('error', None)

        # Make sure either result or error is present
        if result is None and error is None:
            raise ValueError("Either result or error must be present.")
        if result is not None and error is not None:
            raise ValueError("Both result and error cannot be present.")

        # If an error is present, make sure it is an RPCError
        if error is not None:
            error = rpc_error.RPCError.from_dict(error)

        return cls(jsonrpc=jsonrpc, id=id, result=result, error=error)

    def __eq__(self, other) -> bool:
        return all(
            [
                self.id == other.id,
                self.jsonrpc == other.jsonrpc,
                self.result == other.result,
                self.error == other.error,
            ]
        )

    def ok(self) -> bool:
        return all([self.error is None, self.result is not None])


def do_jsonrpc_request(
    data: Union[JsonRPCRequest, RawJsonRPCRequest],
    endpoint: str,
    headers: Dict[str, str] = {"Content-Type": "application/json"},
) -> JsonRPCResponse:
    return JsonRPCResponse.from_raw_dict(
        raw=do_jsonrpc_request_raw(
            data=data,
            endpoint=endpoint,
            headers=headers,
        )
    )


def do_jsonrpc_request_raw(
    data: Union[JsonRPCRequest, RawJsonRPCRequest],
    endpoint: str,
    headers: Dict[str, str] = {"Content-Type": "application/json"},
) -> RawJsonRPCResponse:
    if isinstance(data, dict):
        data = JsonRPCRequest.from_raw_dict(data)
    elif isinstance(data, JsonRPCRequest):
        ...
    # elif  TODO: feat: add a fn that checks the attrs at runtime to
    # assemble a valid JsonRPCRequest even if the class type is not dict
    # or JSONRPCRequest

    resp: requests.Response = requests.post(
        url=endpoint, json=data.to_dict(), headers=headers
    )
    return resp.json()
