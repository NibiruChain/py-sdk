# chain_info_test.py
from typing import Any, Dict, List, Union

import requests

import nibiru
from tests import (  # noqa: F401; pylint: disable=unused-variable
    CONFIG,
    network,
    val_node,
)


def test_genesis_block_ping():
    """Manually query block info from the chain using a get request. This verifies that
    the configuration is valid.
    """
    host = CONFIG.HOST
    block_number = 1
    port = 26657
    url = f"http://{host}:{port}/block?height={block_number}"
    query_resp: Dict[str, Any] = requests.get(url).json()
    assert all([key in query_resp.keys() for key in ["jsonrpc", "id", "result"]])


def test_get_chain_id(val_node: nibiru.Sdk):
    assert CONFIG.CHAIN_ID == val_node.query.get_chain_id()


def test_query_perp_params(val_node: nibiru.Sdk):
    params: Dict[str, Union[float, str]] = val_node.query.perp.params()

    perp_param_names: List[str] = [
        "ecosystemFundFeeRatio",
        "feePoolFeeRatio",
        "liquidationFeeRatio",
        "partialLiquidationRatio",
        "twapLookbackWindow",
    ]
    assert all([(param_name in params) for param_name in perp_param_names])
