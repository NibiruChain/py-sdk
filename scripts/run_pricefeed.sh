#!/bin/bash
set -e

source .env

DEFAULT_CHAIN_ID="nibiru-localnet-0"
DEFAULT_GRPC_ENDPOINT="localhost:9090"
DEFAULT_EXCHANGE_SYMBOLS_MAP='{"bitfinex": {"ubtc:unusd": "tBTCUSD", "ueth:unusd": "tETHUSD", "uusd:unusd": "tUSTUSD"}}'
DEFAULT_FEEDER_MNEMONIC="guard cream sadness conduct invite crumble clock pudding hole grit liar hotel maid produce squeeze return argue turtle know drive eight casino maze host"
DEFAULT_WEBSOCKET_ENDPOINT="ws://localhost:26657/websocket"

if [ -z "$EXCHANGE_SYMBOLS_MAP" ]; then
  EXCHANGE_SYMBOLS_MAP="$DEFAULT_EXCHANGE_SYMBOLS_MAP"
  echo "EXCHANGE_SYMBOLS_MAP='$DEFAULT_EXCHANGE_SYMBOLS_MAP'" >> .env
fi

if [ -z "$CHAIN_ID" ]; then
  CHAIN_ID="$DEFAULT_CHAIN_ID"
  echo "CHAIN_ID='$DEFAULT_CHAIN_ID'" >> .env
fi

if [ -z "$FEEDER_MNEMONIC" ]; then
  FEEDER_MNEMONIC="$DEFAULT_FEEDER_MNEMONIC"
  echo "FEEDER_MNEMONIC='$DEFAULT_FEEDER_MNEMONIC'" >> .env
fi

if [ -z "$GRPC_ENDPOINT" ]; then
  GRPC_ENDPOINT="$DEFAULT_GRPC_ENDPOINT"
  echo "GRPC_ENDPOINT='$DEFAULT_GRPC_ENDPOINT'" >> .env
fi

if [ -z "$WEBSOCKET_ENDPOINT" ]; then
  WEBSOCKET_ENDPOINT="$DEFAULT_WEBSOCKET_ENDPOINT"
  echo "WEBSOCKET_ENDPOINT='$DEFAULT_WEBSOCKET_ENDPOINT'" >> .env
fi


if [ ! pricefeeder ]; then
  echo "Pricefeeder binary does not exist or is not executable."
  echo "Attempting to install binary"
  bash ./scripts/get_pricefeeder.sh
else
  pricefeeder
fi
