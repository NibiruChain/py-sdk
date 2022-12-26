# chain_info_test.py
from typing import Any, Dict, List, Union

import pytest
import requests

import nibiru
from nibiru import pytypes


def test_genesis_block_ping(network: pytypes.Network):
    """Manually query block info from the chain using a get request. This verifies that
    the configuration is valid.
    """
    tendermint_rpc_endpoint = network.tendermint_rpc_endpoint
    query_resp: Dict[str, Any] = requests.get(
        f"{tendermint_rpc_endpoint}/block?height=1"
    ).json()
    assert all([key in query_resp.keys() for key in ["jsonrpc", "id", "result"]])


def test_get_chain_id(sdk_val: nibiru.Sdk):
    assert sdk_val.network.chain_id == sdk_val.query.get_chain_id()


def test_wait_next_block(sdk_val: nibiru.Sdk):
    current_block_height = sdk_val.query.get_latest_block().block.header.height
    sdk_val.query.wait_for_next_block()
    new_block_height = sdk_val.query.get_latest_block().block.header.height

    assert new_block_height > current_block_height


def test_version_works(sdk_val: nibiru.Sdk):
    tests = [
        {"should_fail": False, "versions": ["0.3.2", "0.3.2"]},
        {"should_fail": True, "versions": ["0.3.2", "0.3.4"]},
        {"should_fail": True, "versions": ["0.3.2", "0.4.1"]},
        {"should_fail": True, "versions": ["0.3.2", "1.0.0"]},
        {
            "should_fail": False,
            "versions": ["0.3.2", "master-6a315bab3db46f5fa1158199acc166ed2d192c2f"],
        },
    ]

    for test in tests:
        if test["should_fail"]:
            with pytest.raises(AssertionError, match="Version error"):
                sdk_val.query.assert_compatible_versions(*test["versions"])
        else:
            sdk_val.query.assert_compatible_versions(*test["versions"])


def test_query_perp_params(sdk_val: nibiru.Sdk):
    params: Dict[str, Union[float, str]] = sdk_val.query.perp.params()
    perp_param_names: List[str] = [
        "ecosystemFundFeeRatio",
        "feePoolFeeRatio",
        "liquidationFeeRatio",
        "partialLiquidationRatio",
        "twapLookbackWindow",
    ]
    assert all([(param_name in params) for param_name in perp_param_names])


def test_block_getters(sdk_agent: nibiru.Sdk):
    """Tests queries from the Tendemint gRPC channel
    - GetBlockByHeight
    - GetLatestBlock
    """

    block_by_height_resp = sdk_agent.query.get_block_by_height(2)
    latest_block_resp = sdk_agent.query.get_latest_block()
    block_id_fields: List[str] = ["hash", "part_set_header"]
    block_fields: List[str] = ["data", "evidence", "header", "last_commit"]
    for block_resp in [block_by_height_resp, latest_block_resp]:
        assert all(
            [hasattr(block_resp.block_id, attr) for attr in block_id_fields]
        ), "missing attributes on the 'block_id' field"
        assert all(
            [hasattr(block_resp.block, attr) for attr in block_fields]
        ), "missing attributes on the 'block' field"


def test_blocks_getters(sdk_agent: nibiru.Sdk):
    """Tests queries from the Tendemint gRPC channel
    - GetBlocksByHeight
    """

    block_by_height_resp = sdk_agent.query.get_blocks_by_height(2, 5)
    block_id_fields: List[str] = ["hash", "part_set_header"]
    block_fields: List[str] = ["data", "evidence", "header", "last_commit"]
    for block_resp in block_by_height_resp:
        assert all(
            [hasattr(block_resp.block_id, attr) for attr in block_id_fields]
        ), "missing attributes on the 'block_id' field"
        assert all(
            [hasattr(block_resp.block, attr) for attr in block_fields]
        ), "missing attributes on the 'block' field"


def test_query(sdk_val: nibiru.Sdk):
    """
    Open a position and ensure output is correct
    """
    assert isinstance(sdk_val.query.get_latest_block_height(), int)
    assert isinstance(sdk_val.query.get_version(), str)
