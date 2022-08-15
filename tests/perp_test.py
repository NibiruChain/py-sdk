# perp_test.py
from grpc._channel import _InactiveRpcError

import tests
from nibiru import common

PRECISION = 6


class TestPerp(tests.ModuleTest):
    def test_open_close_position(self):
        """
        Open a position and ensure output is correct
        """

        self.agent = self.create_new_agent_with_funds(
            [common.Coin(1000, "unibi"), common.Coin(1000, "unusd")]
        )

        self.assertRaises(
            _InactiveRpcError,
            self.validator.query.perp.trader_position,
            **{"trader": self.agent.address, "token_pair": self.market},
        )

        tx_output = self.agent.tx.perp.open_position(
            sender=self.agent.address,
            token_pair=self.market,
            side=common.Side.BUY,
            quote_asset_amount=1,
            leverage=10,
            base_asset_amount_limit=0,
        )
        self.validate_tx_output(tx_output)

        # test query position open
        result = self.agent.query.perp.trader_position(
            trader=self.agent.address, token_pair=self.market
        )

        self.assertIsInstance(result, dict)
        print(result)
        self.assertCountEqual(
            result.keys(),
            [
                "block_number",
                "margin_ratio_index",
                "margin_ratio_mark",
                "position",
                "position_notional",
                "unrealized_pnl",
            ],
        )

        self.assertAlmostEqual(result["margin_ratio_index"], 0.1, PRECISION)

        position = result["position"]
        self.assertEqual(position["margin"], 1)
        self.assertEqual(position["open_notional"], 10)
        self.assertAlmostEqual(position["size"], 0.0005, PRECISION)

        # Test add and remove margin
        tx_output = self.agent.tx.perp.add_margin(
            sender=self.agent.address,
            token_pair="ubtc:unusd",
            margin=common.Coin(100, self.market.split(":")[1]),
        )
        self.validate_tx_output(tx_output)

        tx_output = self.agent.tx.perp.remove_margin(
            sender=self.agent.address,
            token_pair="ubtc:unusd",
            margin=common.Coin(100, self.market.split(":")[1]),
        )
        self.validate_tx_output(tx_output)

        # test close position
        result = self.agent.tx.perp.close_position(
            sender=self.agent.address, token_pair=self.market
        )
        self.validate_tx_output(result)

        # test query closed position
        self.assertRaises(
            _InactiveRpcError,
            self.agent.query.perp.trader_position,
            **{"trader": self.agent.address, "token_pair": self.market},
        )
