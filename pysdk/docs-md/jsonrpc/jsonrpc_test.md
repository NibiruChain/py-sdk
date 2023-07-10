Module pysdk.jsonrpc.jsonrpc_test
=================================

Functions
---------


`handle_request(request_json: str) ‑> pysdk.jsonrpc.jsonrpc.JsonRPCResponse`
:


`mock_rpc_method_subtract(params)`
:


`rpc_call_test_case(req: str, resp: str) ‑> Tuple[str, str]`
:


`test_rpc_block_query()`
:   Runs the example query JSON-RPC query from the Tendermint documentation:
    The following exampl

    ```bash
    curl --header "Content-Type: application/json"       --request POST       --data '{"method": "block" , "params": ["5"], "id": 1}'       localhost:26657
    ```

    Ref: https://docs.tendermint.com/v0.37/rpc/#/jsonrpc-http:~:text=block%3Fheight%3D5-,JSONRPC,-/HTTP


`test_rpc_calls(request_json: str, response_json: str)`
:
