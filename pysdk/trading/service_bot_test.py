from typing import Dict, List

import pytest
from service_bot import TradingBot
import pysdk
import tests
from pysdk import Msg
from pysdk import pytypes as pt
import time
import json


def test_make_position():
    bot = TradingBot()
    bot.make_position(50)
    pair = bot.curr_pos.pair
    # Check if response log has appropriate queried fields
    assert bot.pos_dict["OPENED POSITION"][pair]
    tests.dict_keys_must_match(
        bot.pos_dict["OPENED POSITION"][pair],
        [
            "position",
            "position_notional",
            "unrealized_pnl",
            "margin_ratio",
        ],
    )
    position = bot.pos_dict["OPENED POSITION"][pair]["position"]
    assert position["size"]


def test_find_mark_quote():
    # Ensure that the correct fields can be found on nibid markets
    bot = TradingBot()
    bot.find_mark_quote()
    nibid_markets_json = json.loads(bot.nibid_markets)
    for i in range(0, 2):
        nibid_json = nibid_markets_json["amm_markets"][i]
        # use tests.dict_keys_must_match
        """
        Example Return Value Of nibid_json:
            ```json
        {
        "market": {
            "pair": "ubtc:unusd",
            "enabled": true,
            "maintenance_margin_ratio": "0.062500000000000000",
            "max_leverage": "10.000000000000000000",
            "latest_cumulative_premium_fraction": "0.000000000000000000",
            "exchange_fee_ratio": "0.001000000000000000",
            "ecosystem_fund_fee_ratio": "0.001000000000000000",
            "liquidation_fee_ratio": "0.050000000000000000",
            "partial_liquidation_ratio": "0.500000000000000000",
            "funding_rate_epoch_id": "30 min",
            "twap_lookback_window": "1800s",
            "prepaid_bad_debt": {
                "denom": "unusd",
                "amount": "0"
            }
        },
        "amm": {
            "pair": "ubtc:unusd",
            "base_reserve": "30000000008204.776323723603178806",
            "quote_reserve": "29999999991795.223678520341971325",
            "sqrt_depth": "30000000000000.000000000000000000",
            "price_multiplier": "30061.000000000000000000",
            "total_long": "0.000000000000000000",
            "total_short": "8204.776323723603178806"
            }
        }
        ```

        Returns:
            dict: The current market params for the perpetual module
        """

        nibid_amm_json = nibid_json["amm"]
        tests.dict_keys_must_match(
            nibid_amm_json,
            [
                'quote_reserve',
                'base_reserve',
                'price_multiplier',
                'total_long',
                'total_short',
            ],
        )


def test_find_index_quote():
    # Test if exchange rates on oracle exist
    bot = TradingBot()

    """
    Example Return Value Of nibid_exchange_rates_json:
            ```json
    {
        "exchange_rates": [
            {
            "pair": "ubtc:unusd",
            "exchange_rate": "29719.000000000000000000"
            },
            {
            "pair": "ueth:unusd",
            "exchange_rate": "1884.000000000000000000"
            }
        ]
    }
    ```
    """
    bot.find_index_quote()
    nibid_exchange_rates_json = json.loads(bot.nibid_exchange_rates)
    assert nibid_exchange_rates_json["exchange_rates"]


def test_immediate_connection():
    # If chain is running, there should be an immediate connection
    bot = TradingBot()
    time.sleep(15)
    assert bot.connected
