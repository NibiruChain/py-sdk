import json
from typing import Callable, Dict, Tuple, Union

import pytest

from pysdk.jsonrpc import jsonrpc, rpc_error


def mock_rpc_method_subtract(params):
    if isinstance(params, list):
        return params[0] - params[1]
    elif isinstance(params, dict):
        return params["minuend"] - params["subtrahend"]


MOCK_METHODS: Dict[str, Callable] = {"subtract": mock_rpc_method_subtract}


def handle_request(request_json: str) -> jsonrpc.JsonRPCResponse:
    try:
        request_dict = json.loads(request_json)
    except json.JSONDecodeError:
        return jsonrpc.JsonRPCResponse(
            error=rpc_error.ParseError(),
            result=None,
        )

    try:
        request = jsonrpc.JsonRPCRequest.from_raw_dict(request_dict)
    except ValueError:
        return jsonrpc.JsonRPCResponse(
            error=rpc_error.InvalidRequestError(),
            result=None,
            id=request_dict.get("id"),
        )

    method: Union[Callable, None] = MOCK_METHODS.get(request.method)

    if method is None:
        return jsonrpc.JsonRPCResponse(
            id=request.id, error=rpc_error.MethodNotFoundError()
        )
    result = method(request.params)
    return jsonrpc.JsonRPCResponse(id=request.id, result=result)


def rpc_call_test_case(req: str, resp: str) -> Tuple[str, str]:
    assert isinstance(req, str)
    assert isinstance(resp, str)
    return (req, resp)


@pytest.mark.parametrize(
    "request_json, response_json",
    [
        rpc_call_test_case(
            req='{"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": 1}',
            resp='{"jsonrpc": "2.0", "result": 19, "id": 1}',
        ),
        rpc_call_test_case(
            req='{"jsonrpc": "2.0", "method": "subtract", "params": [23, 42], "id": 2}',
            resp='{"jsonrpc": "2.0", "result": -19, "id": 2}',
        ),
        rpc_call_test_case(
            req='{"jsonrpc": "2.0", "method": "subtract", "params": {"subtrahend": 23, "minuend": 42}, "id": 3}',
            resp='{"jsonrpc": "2.0", "result": 19, "id": 3}',
        ),
        rpc_call_test_case(
            req='{"jsonrpc": "2.0", "method": "subtract", "params": {"minuend": 42, "subtrahend": 23}, "id": 4}',
            resp='{"jsonrpc": "2.0", "result": 19, "id": 4}',
        ),
        rpc_call_test_case(
            req='{"jsonrpc": "2.0", "method": "foobar", "id": "1"}',
            resp='{"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": "1"}',
        ),
        rpc_call_test_case(
            req='{"jsonrpc": "2.0", "method": "foobar, "params": "bar", "baz]',
            resp='{"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": null}',
        ),
        rpc_call_test_case(
            req='{"jsonrpc": "2.0", "method": 1, "params": "bar"}',
            resp='{"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": null}',
        ),
    ],
)
def test_rpc_calls(request_json: str, response_json: str):
    got_resp: jsonrpc.JsonRPCResponse = handle_request(request_json)
    want_resp = jsonrpc.JsonRPCResponse.from_raw_dict(
        raw=json.loads(response_json),
    )

    # Manually check equals
    assert got_resp.id == want_resp.id
    assert got_resp.jsonrpc == want_resp.jsonrpc
    assert got_resp.result == want_resp.result
    assert got_resp.error == want_resp.error

    # Check with __eq__ method
    assert got_resp == want_resp


def test_rpc_block_query():
    """
    Runs the example query JSON-RPC query from the Tendermint documentation:
    The following exampl

    ```bash
    curl --header "Content-Type: application/json" \
      --request POST \
      --data '{"method": "block" , "params": ["5"], "id": 1}' \
      localhost:26657
    ```

    Ref: https://docs.tendermint.com/v0.37/rpc/#/jsonrpc-http:~:text=block%3Fheight%3D5-,JSONRPC,-/HTTP
    """

    jsonrpc_resp: jsonrpc.JsonRPCResponse = jsonrpc.do_jsonrpc_request(
        data=dict(method="block", params=["5"], id=1),
    )
    assert isinstance(jsonrpc_resp, jsonrpc.JsonRPCResponse)
    assert jsonrpc_resp.error is None
    assert jsonrpc_resp.result
    assert jsonrpc.JsonRPCResponse.from_raw_dict(raw=jsonrpc_resp.to_dict())
