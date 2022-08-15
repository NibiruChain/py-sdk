from typing import List

from nibiru.client import GrpcClient
from nibiru.common import Coin, TxConfig
from nibiru.composer import Composer
from nibiru.network import Network
from nibiru.sdks.tx.common import BaseTxClient
from nibiru.sdks.tx.dex import DexTxClient
from nibiru.sdks.tx.perp import PerpTxClient
from nibiru.sdks.tx.pricefeed import PricefeedTxClient
from nibiru.wallet import PrivateKey


class TxClient(BaseTxClient):
    def __init__(
        self,
        client: GrpcClient,
        network: Network,
        priv_key: PrivateKey,
        config: TxConfig,
    ):
        super().__init__(
            client=client, network=network, priv_key=priv_key, config=config
        )
        self.dex = DexTxClient(
            client=client, network=network, priv_key=priv_key, config=config
        )
        self.perp = PerpTxClient(
            client=client, network=network, priv_key=priv_key, config=config
        )
        self.pricefeed = PricefeedTxClient(
            client=client, network=network, priv_key=priv_key, config=config
        )

    def msg_send(self, from_address: str, to_address: str, coins: List[Coin], **kwargs):
        msg = Composer.msg_send(
            from_address,
            to_address,
            coins=[coin._generate_proto_object() for coin in coins],
        )
        return super().execute_msg(msg, **kwargs)

    def msg_exec(self, grantee: str, msgs: List, **kwargs):
        msg = Composer.msg_exec(grantee, msgs)
        return super().execute_msg(msg, **kwargs)

    def msg_revoke(self, granter: str, grantee: str, msg_type: str, **kwargs):
        msg = Composer.msg_revoke(granter, grantee, msg_type)
        return super().execute_msg(msg, **kwargs)

    def msg_delegate(
        self, delegator_address: str, validator_address: str, amount: float, **kwargs
    ):
        msg = Composer.msg_delegate(delegator_address, validator_address, amount)
        return super().execute_msg(msg, **kwargs)

    def msg_withdraw_delegator_reward(
        self, delegator_address: str, validator_address: str, **kwargs
    ):
        msg = Composer.msg_withdraw_delegator_reward(
            delegator_address, validator_address
        )
        return super().execute_msg(msg, **kwargs)
