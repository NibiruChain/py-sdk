import dataclasses
import json
import tests
from nibiru.tm_rpc import broadcast
from typing import Optional, List


# This class CANNOT include "Test" in its name because pytest will think it's
# supposed to be a test class.
@dataclasses.dataclass
class TC:
    req_json: str
    happy: bool
    real_tx: bool = False
    err_str: Optional[str] = None


cases: List[TC] = [
    TC(req_json="""{
  "jsonrpc": "2.0",
  "id": 216135382217,
  "method": "broadcast_tx_sync",
  "params": {
    "tx": "CokBCoYBChwvY29zbW9zLmJhbmsudjFiZXRhMS5Nc2dTZW5kEmYKK25pYmkxemFhdnZ6eGV6MGVsdW5kdG4zMnFuazlsa204a21jc3o0NGc3eGwSK25pYmkxYTRyNnhnNHBnNmtkdWZ6cTUydGs1NXZqc3hmYWhjcmF1c2pkYWcaCgoFdW5pYmkSATESbgpQCkYKHy9jb3Ntb3MuY3J5cHRvLnNlY3AyNTZrMS5QdWJLZXkSIwohAvzwBOriY8sVwEXrXf1gXanhT9imlfWeUWLQ8pMxrRsgEgQKAggBGAQSGgoSCgV1bmliaRIJNTY4NzUwMDAwEIDnheBUGkA88j0Oylm+2KqdT/RcxRm28Xe4G8inlGWYRyUbYz+6PQKdQXy3/2UDJ73zCSSBSxNVIUZ5xjufM6oC+6kfWsd3"
  }
}""", happy=True, real_tx=True),
    TC(req_json="""{
  "jsonrpc": "2.0",
  "id": 381619358564,
  "method": "broadcast_tx_sync",
  "params": {
    "tx": "CroDCmoKHi9uaWJpcnUucGVycC52Mi5Nc2dNYXJrZXRPcmRlchJICituaWJpMXphYXZ2enhlejBlbHVuZHRuMzJxbms5bGttOGttY3N6NDRnN3hsEgp1YnRjOnVudXNkGAEiBDEwMDAqAjEwMgEwCmYKHC9uaWJpcnUucGVycC52Mi5Nc2dBZGRNYXJnaW4SRgorbmliaTF6YWF2dnp4ZXowZWx1bmR0bjMycW5rOWxrbThrbWNzejQ0Zzd4bBIKdWJ0Yzp1bnVzZBoLCgV1bnVzZBICMjAKaAofL25pYmlydS5wZXJwLnYyLk1zZ1JlbW92ZU1hcmdpbhJFCituaWJpMXphYXZ2enhlejBlbHVuZHRuMzJxbms5bGttOGttY3N6NDRnN3hsEgp1YnRjOnVudXNkGgoKBXVudXNkEgE1CnoKHi9uaWJpcnUucGVycC52Mi5Nc2dNYXJrZXRPcmRlchJYCituaWJpMXphYXZ2enhlejBlbHVuZHRuMzJxbms5bGttOGttY3N6NDRnN3hsEgp1YnRjOnVudXNkGAIiAzIwMCoTNDAwMDAwMDAwMDAwMDAwMDAwMDIBMBJoClAKRgofL2Nvc21vcy5jcnlwdG8uc2VjcDI1NmsxLlB1YktleRIjCiEC/PAE6uJjyxXARetd/WBdqeFP2KaV9Z5RYtDykzGtGyASBAoCCAEYBRIUCg4KBXVuaWJpEgUxMDAwMBCAtRgaQIjSH+wlldDIfH4XjLPbTq8YIibaRSujNIba5UlpcpkZfQz7feVjtc8OxK+4PW3jGG75ZjJzDQ5ptQ//JbvpINM="
  }
}
    """, happy=True, real_tx=True),
    TC(
        req_json="""
        { "jsonrpc": "2.0", "id": 42, "method": "foobarbat", "params": {}}""",
        happy=False,
        err_str="params.tx of type",
    ),
    TC(
        req_json="""
        { "jsonrpc": "2.0",
          "id": 42,
          "method":
          "foobarbat",
          "params": { "tx": "mock_tx"}
        }""",
        happy=True,
    ),
]


def test_init_BroadcastTxSync():

    for tc in cases:
        try:
            tm_rpc_req = broadcast.BroadcastTxSync(req=json.loads(tc.req_json))

            if not tc.happy:
                raise RuntimeError("expected test case to raise error")
            if tc.real_tx:
                assert tm_rpc_req.params.get("tx")
                # TODO feat: Build tx from string or bytes.
        except BaseException as err:
            if tc.err_str:
                tests.raises(ok_errs=[tc.err_str], err=err)
            assert not tc.happy, "expected test case to pass"
