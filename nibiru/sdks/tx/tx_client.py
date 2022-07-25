from typing import List

from nibiru.client import Client
from nibiru.common import TxConfig
from nibiru.composer import Composer
from nibiru.network import Network
from nibiru.proto.cosmos.base.v1beta1.coin_pb2 import Coin
from nibiru.wallet import PrivateKey

from .common import Tx
from .dex import Dex
from .perp import Perp
from .pricefeed import Pricefeed


class TxClient(Tx):
    def __init__(self, client: Client, network: Network, priv_key: PrivateKey, config: TxConfig):
        super().__init__(client=client, network=network, priv_key=priv_key, config=config)
        self.dex = Dex(client=client, network=network, priv_key=priv_key, config=config)
        self.perp = Perp(client=client, network=network, priv_key=priv_key, config=config)
        self.pricefeed = Pricefeed(client=client, network=network, priv_key=priv_key, config=config)

    def msg_send(self, from_address: str, to_address: str, coins: List[Coin], **kwargs):
        msg = Composer.msg_send(from_address, to_address, coins=coins)
        return super().execute_msg(msg, **kwargs)

    def msg_exec(self, grantee: str, msgs: List, **kwargs):
        msg = Composer.msg_exec(grantee, msgs)
        return super().execute_msg(msg, **kwargs)

    def msg_revoke(self, granter: str, grantee: str, msg_type: str, **kwargs):
        msg = Composer.msg_revoke(granter, grantee, msg_type)
        return super().execute_msg(msg, **kwargs)

    def msg_delegate(self, delegator_address: str, validator_address: str, amount: float, **kwargs):
        msg = Composer.msg_delegate(delegator_address, validator_address, amount)
        return super().execute_msg(msg, **kwargs)

    def msg_withdraw_delegator_reward(self, delegator_address: str, validator_address: str, **kwargs):
        msg = Composer.msg_withdraw_delegator_reward(delegator_address, validator_address)
        return super().execute_msg(msg, **kwargs)
