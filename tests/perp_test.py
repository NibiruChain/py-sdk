# perp_test.py
import unittest

from grpc._channel import _InactiveRpcError

import tests
from nibiru import common


class TestPerp(unittest.TestCase):
    def setUp(self):
        self.validator = tests.get_val_node(tests.get_network())
        self.market = "ubtc:unusd"

    def validate_tx_output(self, tx_output: dict):
        """
        Ensure the output of a transaction have the fields required and that the raw logs are properly parsed

        Args:
            tx_output (dict): The output of a transaction in a dictionary
        """
        self.assertIsInstance(tx_output, dict)
        self.assertCountEqual(
            tx_output.keys(), ['height', 'txhash', 'data', 'rawLog', 'logs', 'gasWanted', 'gasUsed', 'events']
        )
        self.assertIsInstance(tx_output["rawLog"], list)

    def test_open_close_position(self):
        """
        Open a position and ensure output is correct
        """
        tx_output = self.validator.tx.perp.open_position(
            sender=self.validator.address,
            token_pair=self.market,
            side=common.Side.BUY,
            quote_asset_amount=1,
            leverage=10,
            base_asset_amount_limit=0,
        )
        self.validate_tx_output(tx_output)

        # test query position open
        result = self.validator.query.perp.trader_position(trader=self.validator.address, token_pair=self.market)

        self.assertIsInstance(result, dict)
        self.assertCountEqual(
            result.keys(),
            [
                'blockNumber',
                'marginRatioIndex',
                'marginRatioMark',
                'position',
                'positionNotional',
                'unrealizedPnl',
            ],
        )

        # Test add and remove margin
        tx_output = self.validator.tx.perp.add_margin(
            sender=self.validator.address, token_pair="ubtc:unusd", margin=common.Coin(100, self.market.split(":")[1])
        )
        self.validate_tx_output(tx_output)

        tx_output = self.validator.tx.perp.remove_margin(
            sender=self.validator.address, token_pair="ubtc:unusd", margin=common.Coin(100, self.market.split(":")[1])
        )
        self.validate_tx_output(tx_output)

        # test close position
        result = self.validator.tx.perp.close_position(sender=self.validator.address, token_pair=self.market)
        self.validate_tx_output(result)

        # test query closed position
        self.assertRaises(
            _InactiveRpcError,
            self.validator.query.perp.trader_position,
            **{"trader": self.validator.address, "token_pair": self.market},
        )
