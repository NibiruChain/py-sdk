#!/bin/bash

# Define the Python code to be executed

poetry run python <<END
from trading.service_bot import TradingBot

# Instantiate the class
bot = TradingBot()
END
