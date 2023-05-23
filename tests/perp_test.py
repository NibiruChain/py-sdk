# perp_test.py
from typing import Dict, List

import pytest

import nibiru
import tests
from nibiru import Msg
from nibiru import pytypes as pt
from nibiru.exceptions import QueryError

PRECISION = 6

PAIR = "ubtc:unusd"


class ERRORS:
    position_not_found = "collections: not found: 'nibiru.perp.v2.Position'"
    bad_debt = "bad debt"
    underwater_position = "underwater position"


def test_open_position(sdk_val: nibiru.Sdk):
    tests.LOGGER.info("nibid tx perp open-position")
    tx_output: pt.RawTxResp = sdk_val.tx.execute_msgs(
        Msg.perp.open_position(
            sender=sdk_val.address,
            pair=PAIR,
            is_long=False,
            quote_asset_amount=10,
            leverage=10,
            base_asset_amount_limit=0,
        )
    )
    tests.LOGGER.info(
        f"nibid tx perp open-position: {tests.format_response(tx_output)}"
    )
    tests.transaction_must_succeed(tx_output)

    tx_resp = pt.TxResp.from_raw(pt.RawTxResp(tx_output))
    assert "/nibiru.perp.v2.MsgOpenPosition" in tx_resp.rawLog[0].msgs
    events_for_msg: List[str] = [
        "nibiru.perp.v2.PositionChangedEvent",
    ]
    assert all(
        [msg_event in tx_resp.rawLog[0].event_types for msg_event in events_for_msg]
    )


@pytest.mark.order(after="test_open_position")
def test_perp_query_position(sdk_val: nibiru.Sdk):
    try:
        # Trader position must be a dict with specific keys
        position_res = sdk_val.query.perp.position(trader=sdk_val.address, pair=PAIR)
        tests.dict_keys_must_match(
            position_res,
            [
                "block_number",
                "margin_ratio_index",
                "margin_ratio_mark",
                "position",
                "position_notional",
                "unrealized_pnl",
            ],
        )
        tests.LOGGER.info(
            f"nibid query perp trader-position: \n{tests.format_response(position_res)}"
        )

        assert position_res["margin_ratio_mark"]
        position = position_res["position"]
        assert position["margin"]
        assert position["open_notional"]
        assert position["size"]
    except BaseException as err:
        tests.raises(ERRORS.position_not_found, err)


@pytest.mark.order(after="test_perp_query_position")
def test_perp_query_all_positions(sdk_val: nibiru.Sdk):
    positions_map: Dict[str, dict] = sdk_val.query.perp.all_positions(
        trader=sdk_val.address
    )

    if not positions_map:
        return

    pair, position_resp = [item for item in positions_map.items()][0]
    assert len(pair.split(":")) == 2  # check that pair is of form "token0:token1"
    tests.dict_keys_must_match(
        position_resp,
        [
            'position',
            'position_notional',
            'unrealized_pnl',
            'margin_ratio_mark',
            'margin_ratio_index',
            'block_number',
        ],
    )


@pytest.mark.order(after="test_perp_query_all_positions")
def test_perp_add_margin(sdk_val: nibiru.Sdk):
    try:
        # Transaction add_margin must succeed
        tx_output = sdk_val.tx.execute_msgs(
            Msg.perp.add_margin(
                sender=sdk_val.address,
                pair=PAIR,
                margin=pt.Coin(10, "unusd"),
            ),
        )
        tests.LOGGER.info(
            f"nibid tx perp add-margin: \n{tests.format_response(tx_output)}"
        )
    except BaseException as err:
        tests.raises(ERRORS.bad_debt, err)

    # TODO test: verify the margin changes using the events


@pytest.mark.order(after="test_perp_add_margin")
def test_perp_remove_margin(sdk_val: nibiru.Sdk):
    try:
        tx_output = sdk_val.tx.execute_msgs(
            Msg.perp.remove_margin(
                sender=sdk_val.address,
                pair=PAIR,
                margin=pt.Coin(5, "unusd"),
            )
        )
        tests.LOGGER.info(
            f"nibid tx perp remove-margin: \n{tests.format_response(tx_output)}"
        )
        tests.transaction_must_succeed(tx_output)
        # TODO test: verify the margin changes using the events
    except BaseException as err:
        tests.raises(ERRORS.bad_debt, err)


@pytest.mark.order(after="test_perp_remove_margin")
def test_perp_close_posititon(sdk_val: nibiru.Sdk):
    """
    Open a position and ensure output is correct
    """

    try:
        # Transaction close_position must succeed
        tx_output = sdk_val.tx.execute_msgs(
            Msg.perp.close_position(sender=sdk_val.address, pair=PAIR)
        )
        tests.LOGGER.info(
            f"nibid tx perp close-position: \n{tests.format_response(tx_output)}"
        )
        tests.transaction_must_succeed(tx_output)

        # Querying the position should raise an exception if it closed successfully
        with pytest.raises(
            (QueryError, BaseException), match=ERRORS.position_not_found
        ):
            sdk_val.query.perp.position(trader=sdk_val.address, pair=PAIR)
    except BaseException as err:
        expected_errors: List[str] = [
            ERRORS.position_not_found,
            ERRORS.underwater_position,
        ]
        tests.raises(expected_errors, err)
