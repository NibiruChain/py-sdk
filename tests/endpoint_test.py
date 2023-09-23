import requests

import nibiru


def query_chain_id_with_rpc(chain: nibiru.Network) -> str:
    resp: requests.Response = requests.get(f"{chain.tendermint_rpc_endpoint}/status")
    return resp.json()["result"]["node_info"]["network"]


class TestEndpoints:
    @staticmethod
    def test_rpc(network: nibiru.Network) -> None:
        chain_id = query_chain_id_with_rpc(network)
        assert chain_id == network.chain_id

    @staticmethod
    def test_grpc(sdk_val: nibiru.Sdk):
        block_height = sdk_val.query.get_latest_block_height()
        assert block_height > 0
