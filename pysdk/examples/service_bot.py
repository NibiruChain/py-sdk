
import pysdk
import pysdk.msg  # Messages package for transactions
import json
import math
from pysdk import Msg
import subprocess
from typing import Dict, List
import subprocess
from pysdk import pytypes as pt
import tests

class TradingBot:
    # tuning parameters 
    # discrepancy proportion = abs(index - mark)/index
    network = pysdk.Network.localnet()
    pair = "ubtc:unusd"
    wait_time = 60
    has_positions:bool = False
    should_trade:bool = False
    isLong:bool = False
    pos_dict = {"positions": [], "errors": []}
    VALIDATOR_MNEMONIC = "guard cream sadness conduct invite crumble clock pudding hole grit liar hotel maid produce squeeze return argue turtle know drive eight casino maze host"

    tx_config = pysdk.TxConfig(gas_multiplier=3)

    validator = (
    pysdk.Sdk.authorize(
        VALIDATOR_MNEMONIC
    )  # This allows us to recover the wallet with a mnemonic
    .with_network(network)
    .with_config(tx_config)
    )
    sdk_val = tests.fixture_sdk_val()

    def __init__(self):
        mark_quote, quote_asset_reserve = self.find_mark_quote()
        index_quote = self.find_index_quote()
        quote_to_move_price = self.quote_needed_to_move_price(current_price=mark_quote, target_price=index_quote, quote_reserve=quote_asset_reserve)
        should_trade = self.should_make_position(quote_to_move_price,quote_asset_reserve)
        if should_trade:
            self.make_position(quote_to_move_price)
        if not should_trade:
            self.close_position()

    def quote_needed_to_move_price(self,current_price:float, target_price:float, quote_reserve:float) -> float: 
        qp = target_price / current_price
        return -(quote_reserve / math.sqrt(qp) - quote_reserve)


    def should_make_position(self,quote_needed_to_move_price:float,reserves:float) -> float:
        # Check discrepency between mark and index price
        print("Quote to move price: ", quote_needed_to_move_price)
        print("Quote reserves: ", reserves)
        if abs(quote_needed_to_move_price) < 0.1*reserves:
            return False
        else:
            return True
        
    def close_position(self):
        if self.has_positions:
            # close positions
            try:
                # Transaction close_position must succeed
                tx_output = self.sdk_val.tx.execute_msgs(
                    Msg.perp.close_position(sender=self.sdk_val.address, pair=self.pair)
                )
            except BaseException as err:
                self.pos_dict.get("errors").append(str(err))
            self.has_positions = False

    def make_position(self,quote_to_move:int):
        # Make position progressively
        if quote_to_move < 0:
            isLong = False
        else:
            isLong = True
        try:
            tx_output: pt.ExecuteTxResp = self.sdk_val.tx.execute_msgs(
                Msg.perp.open_position(
                    sender=self.sdk_val.address,
                    pair=self.pair,
                    is_long=isLong,
                    quote_asset_amount=quote_to_move,
                    leverage=1,
                    base_asset_amount_limit=0,
                )
            )
            self.pos_dict.get("positions").append(str(tx_output))
            self.has_positions = True
        except BaseException as err:
            self.pos_dict.get("errors").append(str(err))

    def find_index_quote(self) -> float:
        process = subprocess.Popen("nibid q oracle exchange-rates", shell=True, stdout=subprocess.PIPE)
        process.wait()
        data, err = process.communicate()
        if process.returncode is 0:
            nibid_exchange_rates = data.decode('utf-8')
            nibid_exchange_rates_json = json.loads(nibid_exchange_rates)  
            index_quote = float(nibid_exchange_rates_json["exchange_rates"][0]["exchange_rate"])
            index_quote = 2
            print(index_quote)
        else:
            self.pos_dict["errors"].append(err)
        return index_quote

    def find_mark_quote(self) -> float:
        process = subprocess.Popen("nibid q perp markets", shell=True, stdout=subprocess.PIPE)
        process.wait()
        data, err = process.communicate()
        if process.returncode is 0:
            nibid_markets = data.decode('utf-8')
            nibid_markets_json = json.loads(nibid_markets)
            nibid_amm_json = nibid_markets_json["amm_markets"][0]
            quote_asset_reserve = float(nibid_amm_json['amm']['quote_reserve'])
            base_asset_reserve = float(nibid_amm_json['amm']['base_reserve'])
            price_mult = float(nibid_amm_json['amm']['price_multiplier'])
            mark_quote = base_asset_reserve * price_mult/quote_asset_reserve
            print(mark_quote)
        else:
            self.pos_dict["errors"].append(err)
        return mark_quote, quote_asset_reserve
#Write test to check if functions work with asserts
bot = TradingBot()
print(bot.pos_dict)