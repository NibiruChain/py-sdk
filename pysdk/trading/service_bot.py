
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
import time
from pysdk.pytypes import common
import math
import re

class TradingBot:
    # tuning parameters 
    # discrepancy proportion = abs(index - mark)/index
    network = pysdk.Network.customnet()
    pair = "ubtc:unusd"
    wait_time = 60
    has_positions:bool = False
    should_trade:bool = False
    pos_size:float = 0
    isLong:bool = False
    is_against_market:bool = False
    unrealized_pnl: float = 0
    pos_market_delta: float = 0
    pos_dict:Dict = {"positions": [], "errors": []}
    VALIDATOR_MNEMONIC = "guard cream sadness conduct invite crumble clock pudding hole grit liar hotel maid produce squeeze return argue turtle know drive eight casino maze host"

    tx_config = pysdk.TxConfig(broadcast_mode=common.TxBroadcastMode.SYNC, gas_multiplier=1.25, gas_price=0.25)

    validator = (
    pysdk.Sdk.authorize(
        VALIDATOR_MNEMONIC
    )  # This allows us to recover the wallet with a mnemonic
    .with_network(network)
    .with_config(tx_config)
    )
    sdk_val: pysdk.Sdk = tests.fixture_sdk_val()
    
    def __init__(self):

        mark_quote, quote_asset_reserve, net_position, price_multiplier = self.find_mark_quote()
        index_quote = self.find_index_quote()

        print("Market Bias:", net_position)
        quote_to_move_price = self.quote_needed_to_move_price(current_price=mark_quote, target_price=index_quote, quote_reserve=quote_asset_reserve)
        should_trade = self.should_make_position(quote_to_move_price, quote_asset_reserve, net_position)
        if should_trade:
            self.pos_size, self.unrealized_pnl = self.make_position(quote_to_move_price/100)
            # add functionality to close for unrealized pnl and reopen
        if self.has_positions:
            self.is_against_market = self.is_pos_against_market(index_quote, mark_quote)
            self.pos_market_delta = abs((mark_quote - index_quote) * price_multiplier * self.pos_size)

        if not should_trade and self.is_against_market and self.pos_market_delta > 0.1*index_quote:
            self.close_position()
        
        if not self.is_against_market and self.unrealized_pnl > 0.1*self.pos_size:
            self.close_position()
            self.make_position(quote_to_move_price/100)

        #time.sleep(30)
        

    def quote_needed_to_move_price(self, current_price:float, target_price:float, quote_reserve:float) -> float: 
        qp = target_price / current_price
        return -(quote_reserve / math.sqrt(qp) - quote_reserve)


    def should_make_position(self, quote_needed_to_move_price:float, reserves:float, net_position:float) -> float:
        # Check discrepency between mark and index price
        print("Quote To Move Price: ", quote_needed_to_move_price)
        if abs(quote_needed_to_move_price) < 0.05*reserves:
            print("Quote Reserves: ", reserves)
            return False
        else:
            return True
        
    def close_position(self):
        if self.has_positions:
            try:

                positions_map: Dict[str, dict] = self.sdk_val.query.perp.all_positions(
                    trader=self.sdk_val.address
                )

                tx_output = self.sdk_val.tx.execute_msgs(
                    Msg.perp.close_position(sender=self.sdk_val.address, pair=self.pair)
                )
                self.pos_dict.get("positions").append("CLOSED POSITION: " + str(positions_map))
                self.has_positions = False
            except BaseException as err:
                self.pos_dict.get("errors").append(str(err))

    def make_position(self,quote_to_move:int):
        # Make position progressively
        if quote_to_move < 0:
            isLong = False
        else:
            isLong = True
        try:
            self.sdk_val.tx.execute_msgs(
                Msg.perp.open_position(
                    sender=self.sdk_val.address,
                    pair=self.pair,
                    is_long=isLong,
                    quote_asset_amount=abs(quote_to_move),
                    leverage=1,
                    base_asset_amount_limit=0,
                )
            )
            positions_map: Dict[str, dict] = self.sdk_val.query.perp.all_positions(
                trader=self.sdk_val.address
            )

            pos_size = positions_map['ubtc:unusd']['position']['size']
            unrealized_pnl = positions_map['ubtc:unusd']['unrealized_pnl']
            self.pos_dict.get("positions").append("OPENED POSITION: " + str(positions_map))
            self.has_positions = True
        except BaseException as err:
            self.pos_dict.get("errors").append(str(err))
            pos_size = 0
            unrealized_pnl = 0
        return pos_size, unrealized_pnl
       
 
    def find_index_quote(self) -> float:
        process = subprocess.Popen("nibid q oracle exchange-rates", shell=True, stdout=subprocess.PIPE)
        process.wait()
        data, err = process.communicate()
        if process.returncode is 0:
            nibid_exchange_rates = data.decode('utf-8')
            nibid_exchange_rates_json = json.loads(nibid_exchange_rates)  
            if len(nibid_exchange_rates_json["exchange_rates"]) != 0: 
                index_quote = float(nibid_exchange_rates_json["exchange_rates"][0]["exchange_rate"])
            else: 
                self.pos_dict["errors"].append("Exhange Rates unavailable")
                index_quote = 0
            index_quote = 25000
            print("Index Quote: ",index_quote)
        else:
            self.pos_dict["errors"].append(err)
        return index_quote

    def find_mark_quote(self):
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

            net_position = float(nibid_amm_json['amm']['total_long']) - float(nibid_amm_json['amm']['total_short'])

            mark_quote = base_asset_reserve * price_mult/quote_asset_reserve
            print("Mark Quote: ",mark_quote)
        else:
            self.pos_dict["errors"].append(err)
        return mark_quote, quote_asset_reserve, net_position, price_mult
    
    def is_pos_against_market(self, index, mark):
        if mark>index:
            if(self.isLong) == True:
                against_market = True
            else:
                against_market = False
        if index > mark:
            if(self.isLong) == True:
                against_market = False
            else:
                against_market = True
        return against_market

if __name__ == "__main__":
    #Write test to check if functions work with asserts
    bot = TradingBot()
    print("pos_dict", bot.pos_dict)