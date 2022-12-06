import pprint
from typing import Dict, List

import nibiru
import tests
from nibiru import common


def test_query_vpool_reserve_assets(val_node: nibiru.Sdk):
    expected_pairs: List[str] = ["ubtc:unusd", "ueth:unusd"]
    for pair in expected_pairs:
        query_resp: dict = val_node.query.vpool.reserve_assets(pair)
        assert isinstance(query_resp, dict)
        assert query_resp["base_asset_reserve"] > 0
        assert query_resp["quote_asset_reserve"] > 0


def test_query_vpool_all_pools(agent: nibiru.Sdk):
    """Tests deserialization and expected attributes for the
    'nibid query vpool all-pools' command.
    """

    query_resp: Dict[str, List[dict]] = agent.query.vpool.all_pools()
    tests.dict_keys_must_match(query_resp, keys=["pools", "prices"])

    all_vpools: List[dict] = query_resp["pools"]
    vpool_fields: List[str] = [
        "pair",
        "base_asset_reserve",
        "quote_asset_reserve",
        "config",
    ]
    tests.dict_keys_must_match(all_vpools[0], keys=vpool_fields)

    all_vpool_prices = query_resp["prices"]
    price_fields: List[str] = [
        "block_number",
        "index_price",
        "mark_price",
        "swap_invariant",
        "twap_mark",
        "pair",
    ]
    tests.dict_keys_must_match(all_vpool_prices[0], keys=price_fields)

    vpool_prices = all_vpool_prices[0]
    assert isinstance(vpool_prices["block_number"], int), "block_number"
    assert isinstance(vpool_prices["index_price"], float), "index_price"
    assert isinstance(vpool_prices["mark_price"], float), "mark_price"
    assert isinstance(vpool_prices["swap_invariant"], int), "swap_invariant"
    assert isinstance(vpool_prices["twap_mark"], float), "twap_mark"
    assert isinstance(vpool_prices["pair"], str), "pair"
    tests.LOGGER.info(f"vpool_prices: {pprint.pformat(vpool_prices, indent=3)}")


def test_query_vpool_base_asset_price(agent: nibiru.Sdk):
    query_resp: Dict[str, List[dict]] = agent.query.vpool.base_asset_price(
        pair="ueth:unusd", direction=common.Direction.ADD, base_asset_amount="15"
    )
    tests.dict_keys_must_match(query_resp, keys=["price_in_quote_denom"])
    assert isinstance(query_resp["price_in_quote_denom"], float)
    assert query_resp["price_in_quote_denom"] > 0
