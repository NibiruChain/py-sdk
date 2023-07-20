import pysdk
import pysdk.msg  # Messages package for transactions
import json
import math
from pysdk import Msg
import subprocess
from typing import Dict, Tuple, Optional
from pysdk import pytypes as pt
import tests
import time
from pysdk.pytypes import common
import math
import logging
import logging.config
import dataclasses

@dataclasses.dataclass
class PositionState:
    block: int = 0
    size: float = 0
    margin: float = 0
    unrealized_pnl: float = 0
    pair: str = "ubtc:unusd"
    #trader: str
    is_long: bool = False
    has_positions: bool = False
    is_against_market: bool = False
    pos_market_delta: float = False

class TradingBot:

    def __init__(self, validator_mnemonic:str, pair:str, append:bool):
        self.mnemonic = validator_mnemonic
        self.pos_dict = {"positions": []}
        self.tx_config = pysdk.TxConfig(broadcast_mode=common.TxBroadcastMode.SYNC, gas_multiplier=1.25, gas_price=0.25)
        self.network = pysdk.Network.customnet()
        self.connected = False
        self.curr_pos: Optional[PositionState] = PositionState()
        self.curr_pos.pair = pair
        if append:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.run()

    def run(self):
        while not self.connected:
            # Keeps trying to connect to chain if not currently running
            try: 
                self.validator = (
                    pysdk.Sdk.authorize(self.mnemonic)
                    .with_network(self.network)
                    .with_config(self.tx_config)
                )
                self.sdk = tests.fixture_sdk_val()
                self.connected = True 
            except BaseException as err:
                logging.error(err)
                time.sleep(10)

    def should_make_position(self, quote_needed_to_move_price:float, reserves:float, net_position:float) -> bool:
        # Check discrepency between mark and index price
        logging.info("Quote To Move Price: "+ str(quote_needed_to_move_price))
        if abs(quote_needed_to_move_price) < 0.05*reserves:
            logging.info("Quote Reserves: "+ str(reserves))
            return False
        else:
            return True

    # Closes the existing position if the bot has any and logs it   
    def close_position(self, pair:str):
        if self.curr_pos.has_positions:
            try:   
                # Query before closing to store detailed logs
                positions_map: Dict[str, dict] = self.sdk.query.perp.all_positions(
                    trader=self.sdk.address
                )

                self.sdk.tx.execute_msgs(
                    Msg.perp.close_position(sender=self.sdk.address, pair=pair)
                )

                self.pos_dict.get("positions").append("CLOSED POSITION: " + str(positions_map))
                self.curr_pos.has_positions = False
            except BaseException as err:
                logging.error(err)

    # Opens a new position based on the provided quote_to_move and logs it
    def make_position(self, quote_to_move:int):
        if quote_to_move < 0:
            self.curr_pos.is_long = False
        else:
            self.curr_pos.is_long = True
        try:
            self.sdk.tx.execute_msgs(
                Msg.perp.open_position(
                    sender=self.sdk.address,
                    pair=self.curr_pos.pair,
                    is_long=self.curr_pos.is_long,
                    quote_asset_amount=abs(quote_to_move),
                    leverage=1,
                    base_asset_amount_limit=0,
                )
            )

            # Query position to store detailed logs
            positions_map: Dict[str, dict] = self.sdk.query.perp.all_positions(
                trader=self.sdk.address
            )
            pos_size = positions_map[self.curr_pos.pair]['position']['size']
            unrealized_pnl = positions_map[self.curr_pos.pair]['unrealized_pnl']
            self.pos_dict.get("positions").append("OPENED POSITION: " + str(positions_map))
            self.curr_pos.has_positions = True
        except BaseException as err:
            logging.error(err)
            pos_size = 0
            unrealized_pnl = 0
        return pos_size, unrealized_pnl
       
    # Fetch the index from chain
    def find_index_quote(self) -> float:
        process = subprocess.Popen("nibid q oracle exchange-rates", shell=True, stdout=subprocess.PIPE)
        process.wait()
        data, err = process.communicate()
        if process.returncode == 0:
            index_quote = self.parse_index_quote(data)
        else:
            logging.error(err)
        return index_quote
    
    def parse_index_quote(self, data: bytes) -> float:
        self.nibid_exchange_rates = data.decode('utf-8')
        nibid_exchange_rates_json = json.loads(self.nibid_exchange_rates)  
        if len(nibid_exchange_rates_json["exchange_rates"]) != 0: 
            index_quote = float(nibid_exchange_rates_json["exchange_rates"][0]["exchange_rate"])
        else: 
            logging.error("Exhange Rates unavailable")
            index_quote = 2000
        index_quote = 25000
        return index_quote
    
    # Fetch the mark, price_mult, quote reserves, and market bias from chain
    def find_mark_quote(self) -> Tuple[float, float, float, float]:
        process = subprocess.Popen("nibid q perp markets", shell=True, stdout=subprocess.PIPE)
        process.wait()
        data, err = process.communicate()
        if process.returncode == 0:
            mark_quote, quote_asset_reserve, net_position, price_mult = self.parse_mark_quote(data)
            logging.info("Mark Quote: "+str(mark_quote))

        else:
            logging.error(err)
        return mark_quote, quote_asset_reserve, net_position, price_mult
    
    def parse_mark_quote(self, data: bytes) -> Tuple[float, float, float]:
        self.nibid_markets = data.decode('utf-8')
        nibid_markets_json = json.loads(self.nibid_markets)
        if self.curr_pos.pair == "ubtc:unusd":
            query_pos = 0
        if self.curr_pos.pair == "ueth:unusd":
            query_pos = 1
        nibid_amm_json = nibid_markets_json["amm_markets"][query_pos]
        quote_asset_reserve = float(nibid_amm_json['amm']['quote_reserve'])
        base_asset_reserve = float(nibid_amm_json['amm']['base_reserve'])
        price_mult = float(nibid_amm_json['amm']['price_multiplier'])
        net_position = float(nibid_amm_json['amm']['total_long']) - float(nibid_amm_json['amm']['total_short'])

        mark_quote = base_asset_reserve * price_mult/quote_asset_reserve

        return mark_quote, quote_asset_reserve, net_position, price_mult

    
    # Check if the position is against the market based on mark & index
    def is_pos_against_market(self, pos_size: float, mark: float, index: float) -> bool:
        market_long: bool = mark > index
        pos_long: bool = pos_size >= 0
        return market_long != pos_long
        
    # Calculate the quote needed to move the price to reach the target price
    def quote_needed_to_move_price(self, current_price:float, target_price:float, quote_reserve:float) -> float: 
        qp = target_price / current_price
        return -(quote_reserve / math.sqrt(qp) - quote_reserve) 


def main():
    # Instantiate the TradingBot class within the main() function
    while True:
        bot = TradingBot(
            validator_mnemonic="guard cream sadness conduct invite crumble clock pudding hole grit liar hotel maid produce squeeze return argue turtle know drive eight casino maze host",
            pair = "ubtc:unusd",
            append = True
            )
        mark_quote, quote_asset_reserve, net_position, price_multiplier = bot.find_mark_quote()
        index_quote = bot.find_index_quote()
        logging.info("Index Quote: "+ str(index_quote))

        logging.info("Market Bias:"+ str(net_position))

        quote_to_move_price = bot.quote_needed_to_move_price(current_price=mark_quote, target_price=index_quote, quote_reserve=quote_asset_reserve)
        should_trade = bot.should_make_position(quote_to_move_price, quote_asset_reserve, net_position)

        if should_trade and not bot.curr_pos.has_positions:
            bot.curr_pos.size, bot.curr_pos.unrealized_pnl = bot.make_position(quote_to_move_price/1000000)

        if bot.curr_pos.has_positions:
            bot.curr_pos.is_against_market = bot.is_pos_against_market(bot.curr_pos.size, index_quote, mark_quote)
            bot.curr_pos.pos_market_delta = abs((mark_quote - index_quote) * price_multiplier * bot.curr_pos.size)

        if not should_trade and bot.curr_pos.is_against_market and bot.curr_pos.pos_market_delta > 0.1*index_quote:
            bot.close_position(pair=bot.curr_pos.pair)

        if not bot.curr_pos.is_against_market and bot.curr_pos.unrealized_pnl > 0.1*abs(bot.curr_pos.size):
            bot.close_position()
            bot.make_position(quote_to_move_price/100)
               
        #self.sdk.query.perp.params()
        logging.info(str(bot.pos_dict))
        time.sleep(15)

if __name__ == "__main__":
    main()
