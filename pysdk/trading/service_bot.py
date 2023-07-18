import pysdk
import pysdk.msg  # Messages package for transactions
import json
import math
from pysdk import Msg
import subprocess
from typing import Dict, List, Tuple
from pysdk import pytypes as pt
import tests
import time
from pysdk.pytypes import common
import math

class TradingBot:

    def __init__(self):
        self.pair = "ubtc:unusd"
        self.wait_time = 60
        self.has_positions = False
        self.should_trade = False
        self.pos_size = 0
        self.isLong = False
        self.is_against_market = False
        self.unrealized_pnl = 0
        self.pos_market_delta = 0
        self.pos_dict = {"positions": [], "errors": []}
        self.VALIDATOR_MNEMONIC = "guard cream sadness conduct invite crumble clock pudding hole grit liar hotel maid produce squeeze return argue turtle know drive eight casino maze host"
        self.tx_config = pysdk.TxConfig(broadcast_mode=common.TxBroadcastMode.SYNC, gas_multiplier=1.25, gas_price=0.25)
        self.network = pysdk.Network.customnet()
        self.connected = False

        while not self.connected:
            # Keeps trying to connect to chain if not currently running
            try: 
                self.validator = (
                    pysdk.Sdk.authorize(self.VALIDATOR_MNEMONIC)
                    .with_network(self.network)
                    .with_config(self.tx_config)
                )
                self.sdk_val = tests.fixture_sdk_val()
                self.connected = True 
            except BaseException as err:
                print("error: ", err)
                time.sleep(10)

    def should_make_position(self, quote_needed_to_move_price:float, reserves:float, net_position:float) -> bool:
        # Check discrepency between mark and index price
        print("Quote To Move Price: ", quote_needed_to_move_price)
        if abs(quote_needed_to_move_price) < 0.05*reserves:
            print("Quote Reserves: ", reserves)
            return False
        else:
            return True

    # Closes the existing position if the bot has any and logs it   
    def close_position(self):
        if self.has_positions:
            try:   
                # Query before closing to store detailed logs
                positions_map: Dict[str, dict] = self.sdk_val.query.perp.all_positions(
                    trader=self.sdk_val.address
                )

                self.sdk_val.tx.execute_msgs(
                    Msg.perp.close_position(sender=self.sdk_val.address, pair=self.pair)
                )

                self.pos_dict.get("positions").append("CLOSED POSITION: " + str(positions_map))
                self.has_positions = False
            except BaseException as err:
                self.pos_dict.get("errors").append(str(err))

    # Opens a new position based on the provided quote_to_move and logs it
    def make_position(self, quote_to_move:int):
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

            # Query position to store detailed logs
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
       
    # Fetch the index from chain
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
    
    # Fetch the mark, price_mult, quote reserves, and market bias from chain
    def find_mark_quote(self) -> Tuple[float, float, float, float]:
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
    
    # Check if the position is against the market based on mark & index
    def is_pos_against_market(self, index, mark) -> bool:
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
        
        
    # Calculate the quote needed to move the price to reach the target price
    def quote_needed_to_move_price(self, current_price:float, target_price:float, quote_reserve:float) -> float: 
        qp = target_price / current_price
        return -(quote_reserve / math.sqrt(qp) - quote_reserve)  


def main():
    # Instantiate the TradingBot class within the main() function
    while True:
        bot = TradingBot()

        mark_quote, quote_asset_reserve, net_position, price_multiplier = bot.find_mark_quote()
        index_quote = bot.find_index_quote()

        print("Market Bias:", net_position)
        quote_to_move_price = bot.quote_needed_to_move_price(current_price=mark_quote, target_price=index_quote, quote_reserve=quote_asset_reserve)
        should_trade = bot.should_make_position(quote_to_move_price, quote_asset_reserve, net_position)

        if should_trade and not bot.has_positions:
            bot.pos_size, bot.unrealized_pnl = bot.make_position(quote_to_move_price/100)

        if bot.has_positions:
            bot.is_against_market = bot.is_pos_against_market(index_quote, mark_quote)
            bot.pos_market_delta = abs((mark_quote - index_quote) * price_multiplier * bot.pos_size)

        if not should_trade and bot.is_against_market and bot.pos_market_delta > 0.1*index_quote:
            bot.close_position()

        if not bot.is_against_market and bot.unrealized_pnl > 0.1*abs(bot.pos_size):
            bot.close_position()
            bot.make_position(quote_to_move_price/100)

        print("LOGS: " + str(bot.pos_dict))

        time.sleep(15)

if __name__ == "__main__":
    main()
    #Write test to check if functions work with asserts

