import requests

import nibiru as nb


def query_chain_id_with_rest(chain: nb.Network) -> str:
    resp: requests.Response = requests.get(f"{chain.lcd_endpoint}/node_info")
    return resp.json()["node_info"]["network"]


def query_chain_id_with_rpc(chain: nb.Network) -> str:
    resp: requests.Response = requests.get(f"{chain.tendermint_rpc_endpoint}/status")
    return resp.json()["result"]["node_info"]["network"]


class TestEndpoints:
    @staticmethod
    def test_rpc(network: nb.Network) -> bool:
        chain_id = query_chain_id_with_rpc(network)
        assert chain_id == network.chain_id

    @staticmethod
    def test_lcd_rest(network: nb.Network):
        chain_id = query_chain_id_with_rest(network)
        assert chain_id == network.chain_id

    @staticmethod
    def test_grpc(sdk_val: nb.Sdk):
        block_height = sdk_val.query.get_latest_block_height()
        assert block_height > 0
