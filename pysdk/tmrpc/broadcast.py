import abc
import base64
import dataclasses
import json
from typing import Any, Callable, Dict, Optional, Tuple, Union

from pysdk.jsonrpc import jsonrpc


class TypedJsonRpcRequest(abc.ABC, jsonrpc.JsonRPCRequest):
    @abc.abstractmethod
    def create(cls, *args) -> jsonrpc.JsonRPCRequest:
        """TODO docs"""

    @classmethod
    @abc.abstractmethod
    def _validate_tm_rpc_request(*args):
        """TODO docs"""


@dataclasses.dataclass
class BroadcastTxSync(jsonrpc.JsonRPCRequest):
    """TODO docs

    Args:
        req (Union[jsonrpc.JsonRPCRequest, str, dict]): An object that can be
            parsed as a jsonrpc.JsonRPCRequest.
    """

    def __new__(
        cls,
        req: Union[jsonrpc.JsonRPCRequest, str, dict],
    ) -> "BroadcastTxSync":
        if isinstance(req, jsonrpc.JsonRPCRequest):
            cls._validate_tm_rpc_request(json_rpc_req=req)
            return req
        elif isinstance(req, dict):
            json_rpc_req: jsonrpc.JsonRPCRequest = jsonrpc.JsonRPCRequest.from_raw_dict(
                raw=req
            )
            return cls(req=json_rpc_req)
        elif isinstance(req, str):
            req_dict: dict = json.loads(req)
            json_rpc_req: jsonrpc.JsonRPCRequest = jsonrpc.JsonRPCRequest.from_raw_dict(
                raw=req_dict
            )
            return cls(req=json_rpc_req)
        else:
            raise TypeError(
                'expected request of type "jsonrpc.JsonRPCRequest", "str" or '
                + f'"dict": got type {type(req)}'
            )

    def create(
        tx_raw_bytes: Union[bytes, str],
        id=None,
    ) -> jsonrpc.JsonRPCRequest:
        tx_raw: str
        if isinstance(tx_raw_bytes, bytes):
            tx_raw = base64.b64encode(tx_raw_bytes).decode()
        elif isinstance(tx_raw_bytes, str):
            tx_raw = base64.b64decode(tx_raw_bytes).decode()
        else:
            raise TypeError(
                "expected 'tx_raw_bytes' of type Union[str, bytes]"
                + f", got type {type(tx_raw_bytes)}"
            )

        return jsonrpc.JsonRPCRequest(
            method="broadcast_tx_sync",
            params=dict(tx=tx_raw),
            id=id,
        )

    @classmethod
    def _validate_tm_rpc_request(cls, json_rpc_req: jsonrpc.JsonRPCRequest):
        if not isinstance(json_rpc_req.params, dict):
            raise TypeError(
                f"params field of {cls.__name__} must be a dict"
                + f", not type {type(json_rpc_req.params)}",
            )

        tx_bytes = json_rpc_req.params.get("tx")
        if not isinstance(tx_bytes, (str, bytes)):
            raise TypeError(
                f"request type {cls.__name__} must have "
                + "params.tx of type Union[str, bytes]"
                + f", not {type(tx_bytes).__name__}"
            )


CHAIN_JSON_RPC_METHODS: Dict[str, Callable[[Any], jsonrpc.JsonRPCRequest]] = dict(
    broadcast_tx_sync=BroadcastTxSync.create,
)


# TODO test
def is_known_rpc_method(method: str) -> Tuple[bool, Optional[Callable]]:
    method_fn = CHAIN_JSON_RPC_METHODS.get(method)
    if method_fn is None:
        return False, method_fn
    return True, method_fn
