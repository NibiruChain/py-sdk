# # Copyright 2022 Nibiru Labs
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.

# import logging

# from nibiru.composer import Composer as ProtoMsgComposer
# from nibiru.client import Client
# from nibiru.transaction import Transaction
# from nibiru.network import Network
# from nibiru.wallet import PrivateKey, Address


# def main() -> None:
#     # select network: local, testnet, mainnet
#     network = Network.local()
#     composer = ProtoMsgComposer(network=network.string())

#     # initialize grpc client
#     client = Client(network, insecure=True)
#     client.sync_timeout_height()

#     # load account
#     priv_key = PrivateKey.from_mnemonic("guard cream sadness conduct invite crumble clock pudding hole grit liar hotel maid produce squeeze return argue turtle know drive eight casino maze host")
#     pub_key = priv_key.to_public_key()
#     address = pub_key.to_address().init_num_seq(network.lcd_endpoint)

#     # prepare tx msg
#     market_id = "0x0511ddc4e6586f3bfe1acb2dd905f8b8a82c97e1edaef654b12ca7e6031ca0fa"

#     grantee = "inj1hkhdaj2a2clmq5jq6mspsggqs32vynpk228q3r"
#     granter_inj_address = "inj14au322k9munkmx5wrchz9q30juf5wjgz2cfqku"
#     granter_address = Address.from_acc_bech32(granter_inj_address)
#     granter_subaccount_id = granter_address.get_subaccount_id(index=0)
#     msg0 = composer.MsgCreateSpotLimitOrder(
#         sender=granter_inj_address,
#         market_id=market_id,
#         subaccount_id=granter_subaccount_id,
#         fee_recipient=grantee,
#         price=7.523,
#         quantity=0.01,
#         is_buy=True,
#         is_po=False
#     )

#     msg = composer.msg_exec(
#         grantee=grantee,
#         msgs=[msg0]
#     )

#     # build sim tx
#     tx = (
#         Transaction()
#         .with_messages(msg)
#         .with_sequence(address.get_sequence())
#         .with_account_num(address.get_number())
#         .with_chain_id(network.chain_id)
#         .with_signer(priv_key)
#     )
#     sim_tx_raw_bytes = tx.get_signed_tx_data()

#     # simulate tx
#     (sim_res, success) = client.simulate_tx(sim_tx_raw_bytes)
#     if not success:
#         print(sim_res)
#         return

#     sim_res_msg = ProtoMsgComposer.MsgResponses(sim_res.result.data, simulation=True)
#     print(sim_res_msg)
#     unpacked_msg_res = ProtoMsgComposer.UnpackMsgExecResponse(
#         msg_type=msg0.__class__.__name__,
#         data=sim_res_msg[0]
#     )
#     print("simulation msg response")
#     print(unpacked_msg_res)

#     # build tx
#     gas_price = 500000000
#     gas_limit = sim_res.gas_info.gas_used + 20000 # add 20k for gas, fee computation
#     gas_fee = '{:.18f}'.format((gas_price * gas_limit) / pow(10, 18)).rstrip('0')
#     fee = [composer.Coin(
#         amount=gas_price * gas_limit,
#         denom=network.fee_denom,
#     )]
#     tx = tx.with_gas(gas_limit).with_fee(fee).with_memo('').with_timeout_height(client.timeout_height)
#     tx_raw_bytes = tx.get_signed_tx_data()

#     # broadcast tx: send_tx_async_mode, send_tx_sync_mode, send_tx_block_mode
#     res = client.send_tx_sync_mode(tx_raw_bytes)
#     print(res)
#     print("gas wanted: {}".format(gas_limit))
#     print("gas fee: {} unibi".format(gas_fee))

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     main()
