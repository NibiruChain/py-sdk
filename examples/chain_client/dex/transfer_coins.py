# Copyright 2022 Nibiru Labs
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import logging

from nibiru.composer import Composer, PoolAsset
from nibiru.client import Client
from nibiru.transaction import Transaction
from nibiru.network import Network
from nibiru.wallet import PrivateKey


async def main() -> None:
    # select network: local, testnet, mainnet
    network = Network.local()
    composer = Composer(network=network.string())

    # initialize grpc client
    client = Client(network, insecure=True)
    await client.sync_timeout_height()

    priv_key = PrivateKey.from_mnemonic("guard cream sadness conduct invite crumble clock pudding hole grit liar hotel maid produce squeeze return argue turtle know drive eight casino maze host")
    pub_key = priv_key.to_public_key()
    address = await pub_key.to_address().async_init_num_seq(network.lcd_endpoint)

    # prepare tx msg
    msg = composer.dex.create_pool(
        creator=address.to_acc_bech32(),
        swap_fee="2",
        exit_fee="3",
        assets=[
            PoolAsset(token=composer.Coin(4, "unusd"),weight="3"),
            PoolAsset(token=composer.Coin(5, "uusdc"),weight="4"),
        ],
    )

    # build sim tx
    tx = (
        Transaction()
        .with_messages(msg)
        .with_sequence(address.get_sequence())
        .with_account_num(address.get_number())
        .with_chain_id(network.chain_id)
        .with_signer(priv_key)
    )
    sim_tx_raw_bytes = tx.get_signed_tx_data()

    # simulate tx
    (sim_res, success) = await client.simulate_tx(sim_tx_raw_bytes)
    if not success:
        print(sim_res)
        return

    # build tx
    gas_price = 1
    gas_limit = sim_res.gas_info.gas_used + 2  # add 2 for gas, fee computation
    gas_fee = '{:.18f}'.format((gas_price * gas_limit) / pow(10, 18)).rstrip('0')
    fee = [composer.Coin(
        amount=gas_price * gas_limit,
        denom=network.fee_denom,
    )]
    tx = tx.with_gas(gas_limit).with_fee(fee).with_memo('').with_timeout_height(client.timeout_height)
    tx_raw_bytes = tx.get_signed_tx_data()

    # broadcast tx: send_tx_async_mode, send_tx_sync_mode, send_tx_block_mode
    res = await client.send_tx_sync_mode(tx_raw_bytes)
    print(res)
    print("gas wanted: {}".format(gas_limit))
    print("gas fee: {} unibi".format(gas_fee))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(main())
