# chain_info_test.py
import dataclasses
from typing import Any, Dict, List, Union

import pytest
import requests

import nibiru
import tests
from nibiru import ChainClient, Network


def test_genesis_block_ping(network: Network):
    """Manually query block info from the chain using a get request. This verifies that
    the configuration is valid.
    """
    tendermint_rpc_endpoint = network.tendermint_rpc_endpoint
    query_resp: Dict[str, Any] = requests.get(
        f"{tendermint_rpc_endpoint}/block?height=1"
    ).json()
    assert all([key in query_resp.keys() for key in ["jsonrpc", "id", "result"]])


def test_get_chain_id(client_validator: ChainClient):
    assert client_validator.network.chain_id == client_validator.query.get_chain_id()


def test_wait_next_block(client_validator: ChainClient):
    ...


#     current_block_height = client_validator.query.get_latest_block().block.header.height
#     client_validator.query.wait_for_next_block()
#     new_block_height = client_validator.query.get_latest_block().block.header.height

#     assert new_block_height > current_block_height


def test_version_works(client_validator: ChainClient):
    test_cases: List[Dict[str, Union[bool, List[str]]]] = [
        {"should_fail": False, "versions": ["0.3.2", "0.3.2"]},
        {"should_fail": False, "versions": ["0.3.2", "0.3.4"]},
        {"should_fail": True, "versions": ["0.3.2", "0.4.1"]},
        {"should_fail": True, "versions": ["0.3.2", "1.0.0"]},
        {
            "should_fail": False,
            "versions": ["0.3.2", "master-6a315bab3db46f5fa1158199acc166ed2d192c2f"],
        },
    ]

    for tc in test_cases:
        if tc["should_fail"]:
            with pytest.raises(AssertionError, match="Version error"):
                assert isinstance(tc["versions"], list)
                client_validator.query.assert_compatible_versions(*tc["versions"])
        else:
            assert isinstance(tc["versions"], list)
            client_validator.query.assert_compatible_versions(*tc["versions"])


def test_block_getters(client_new_user: ChainClient):
    """Tests queries from the Tendemint gRPC channel
    - GetBlockByHeight
    - GetLatestBlock
    """

    block_by_height_resp = client_new_user.query.get_block_by_height(2)
    latest_block_resp = client_new_user.query.get_latest_block()
    block_id_fields: List[str] = ["hash", "part_set_header"]
    block_fields: List[str] = ["data", "evidence", "header", "last_commit"]
    for block_resp in [block_by_height_resp, latest_block_resp]:
        assert all(
            [hasattr(block_resp.block_id, attr) for attr in block_id_fields]
        ), "missing attributes on the 'block_id' field"
        assert all(
            [hasattr(block_resp.block, attr) for attr in block_fields]
        ), "missing attributes on the 'block' field"


def test_blocks_getters(client_new_user: ChainClient):
    """Tests queries from the Tendemint gRPC channel
    - GetBlocksByHeight
    """

    block_by_height_resp = client_new_user.query.get_blocks_by_height(2, 5)
    block_id_fields: List[str] = ["hash", "part_set_header"]
    block_fields: List[str] = ["data", "evidence", "header", "last_commit"]
    for block_resp in block_by_height_resp:
        assert all(
            [hasattr(block_resp.block_id, attr) for attr in block_id_fields]
        ), "missing attributes on the 'block_id' field"
        assert all(
            [hasattr(block_resp.block, attr) for attr in block_fields]
        ), "missing attributes on the 'block' field"


def test_query(client_validator: ChainClient):
    """
    Open a position and ensure output is correct
    """
    assert isinstance(client_validator.query.get_latest_block_height(), int)
    assert isinstance(client_validator.query.get_version(), str)


def test_network_from_chain_id():
    @dataclasses.dataclass
    class Case:
        chain_id_in: str
        expected_fail: bool = False

    def run_case(test_case: Case):
        if test_case.expected_fail:
            try:
                _ = nibiru.Network.from_chain_id(test_case.chain_id_in)
            except BaseException as err:
                tests.raises(["invalid chain type", "invalid chain_id format"], err)
        else:
            network = nibiru.Network.from_chain_id(test_case.chain_id_in)
            _, chain_type, _ = network.chain_id.split("-")

            if chain_type == "localnet":
                return

            assert chain_type in network.tendermint_rpc_endpoint
            assert chain_type in network.lcd_endpoint
            assert chain_type in network.grpc_endpoint

    for test_case in [
        Case("nibiru-devnet-4"),
        Case("nibiru-randnet-123", expected_fail=True),
        Case("nibiru-testnet-685920"),
        Case("xxx-yyy", expected_fail=True),
        Case("nibiru-localnet-78"),
    ]:
        run_case(test_case=test_case)
