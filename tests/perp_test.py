# perp_test.py
from typing import Dict, List

import pytest

import tests
from nibiru import Msg
from nibiru import pytypes as pt
from nibiru.utils import assert_subset

PRECISION = 6

PAIR = "ubtc:unusd"


class ERRORS:
    collections_not_found = "collections: not found"
    bad_debt = "bad debt"
    underwater_position = "underwater position"
    no_prices = "no valid prices available"


def test_open_position(client_validator):
    tests.LOGGER.info("nibid tx perp open-position")
    try:
        tx_output: pt.ExecuteTxResp = client_validator.tx.execute_msgs(
            Msg.perp.open_position(
                pair=PAIR,
                is_long=False,
                quote_asset_amount=10,
                leverage=10,
                base_asset_amount_limit=0,
            )
        )
        tests.broadcast_tx_must_succeed(res=tx_output)
    except BaseException as err:
        ok_errors: List[str] = [ERRORS.no_prices]
        tests.raises(ok_errors, err)
        if ERRORS.no_prices in f"{err}":
            tests.LOGGER.info("Exchange rates unavailable, please run pricefeeder")


@pytest.mark.order(after="test_open_position")
def test_perp_query_position(client_validator):
    try:
        # Trader position must be a dict with specific keys
        position_res = client_validator.query.perp.position(
            trader=client_validator.address, pair=PAIR
        )
        tests.dict_keys_must_match(
            position_res,
            [
                "position",
                "position_notional",
                "unrealized_pnl",
                "margin_ratio",
            ],
        )
        position = position_res["position"]
        assert position["margin"]
        assert position["open_notional"]
        assert position["size"]
    except BaseException as err:
        ok_errors: List[str] = [ERRORS.collections_not_found]
        tests.raises(ok_errors, err)


def test_perp_query_market(client_validator):
    output = client_validator.query.perp.markets()

    expected_to_be_equal = {
        "ammMarkets": [
            {
                "market": {
                    "pair": "ubtc:unusd",
                    "enabled": True,
                    "maintenanceMarginRatio": 0.0625,
                    "maxLeverage": 10.0,
                    "latestCumulativePremiumFraction": 0.0,
                    "exchangeFeeRatio": 0.001,
                    "ecosystemFundFeeRatio": 0.001,
                    "liquidationFeeRatio": 0.05,
                    "partialLiquidationRatio": 0.5,
                    "fundingRateEpochId": "30 min",
                    "twapLookbackWindow": "1800s",
                    "prepaidBadDebt": {"denom": "unusd", "amount": "0"},
                },
                "amm": {
                    "pair": "ubtc:unusd",
                    "sqrtDepth": 30000000000000.0,
                },
            },
            {
                "market": {
                    "pair": "ueth:unusd",
                    "enabled": True,
                    "maintenanceMarginRatio": 0.0625,
                    "maxLeverage": 10.0,
                    "latestCumulativePremiumFraction": 0.0,
                    "exchangeFeeRatio": 0.001,
                    "ecosystemFundFeeRatio": 0.001,
                    "liquidationFeeRatio": 0.05,
                    "partialLiquidationRatio": 0.5,
                    "fundingRateEpochId": "30 min",
                    "twapLookbackWindow": "1800s",
                    "prepaidBadDebt": {"denom": "unusd", "amount": "0"},
                },
                "amm": {
                    "pair": "ueth:unusd",
                    "sqrtDepth": 30000000000000.0,
                },
            },
        ]
    }

    # test subset, exclude changing baseReserve, quoteReserve, totalLong, totalShort
    assert_subset(output, expected_to_be_equal)


@pytest.mark.order(after="test_perp_query_position")
def test_perp_query_all_positions(client_validator):
    positions_map: Dict[str, dict] = client_validator.query.perp.all_positions(
        trader=client_validator.address
    )

    if not positions_map:
        return

    pair, position_resp = [item for item in positions_map.items()][0]
    # check that pair is of form "token0:token1"
    assert len(pair.split(":")) == 2
    tests.dict_keys_must_match(
        position_resp,
        [
            "position",
            "position_notional",
            "unrealized_pnl",
            "margin_ratio",
        ],
    )


@pytest.mark.order(after="test_perp_query_all_positions")
def test_perp_add_margin(client_validator):
    try:
        # Transaction add_margin must succeed
        tx_output = client_validator.tx.execute_msgs(
            Msg.perp.add_margin(
                pair=PAIR,
                margin=pt.Coin(10, "unusd"),
            ),
        )
        tests.broadcast_tx_must_succeed(res=tx_output)
        # TODO deprecated
        # tests.LOGGER.info(
        #     f"nibid tx perp add-margin: \n{tests.format_response(tx_output)}"
        # )
    except BaseException as err:
        ok_errors: List[str] = [ERRORS.collections_not_found, ERRORS.bad_debt]
        tests.raises(ok_errors, err)

    # TODO test: verify the margin changes using the events


@pytest.mark.order(after="test_perp_add_margin")
def test_perp_remove_margin(client_validator):
    try:
        tx_output = client_validator.tx.execute_msgs(
            Msg.perp.remove_margin(
                pair=PAIR,
                margin=pt.Coin(2, "unusd"),
            )
        )
        tests.broadcast_tx_must_succeed(res=tx_output)
        # TODO test: verify the margin changes using the events
    except BaseException as err:
        ok_errors: List[str] = [ERRORS.collections_not_found, ERRORS.bad_debt]
        tests.raises(ok_errors, err)


@pytest.mark.order(after="test_perp_remove_margin")
def test_perp_close_posititon(client_validator):
    """
    Open a position and ensure output is correct
    """

    try:
        # Transaction close_position must succeed
        tx_output = client_validator.tx.execute_msgs(Msg.perp.close_position(pair=PAIR))
        tests.broadcast_tx_must_succeed(res=tx_output)

        out = client_validator.query.perp.position(
            trader=client_validator.address, pair=PAIR
        )
        # Querying the position should raise an exception if it closed
        # successfully
        # with pytest.raises(
        #      (QueryError, BaseException), match=ERRORS.collections_not_found
        # ):
        assert out  # TODO: replace with actual checks.

    except BaseException as err:
        ok_errors: List[str] = [
            ERRORS.collections_not_found,
            ERRORS.underwater_position,
            ERRORS.no_prices,
        ]
        tests.raises(ok_errors, err)
