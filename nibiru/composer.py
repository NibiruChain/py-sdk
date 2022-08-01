from typing import List

from google.protobuf import any_pb2

from .composers import Pricefeed
from .proto.cosmos.authz.v1beta1 import tx_pb2 as cosmos_authz_tx_pb
from .proto.cosmos.bank.v1beta1 import tx_pb2 as cosmos_bank_tx_pb
from .proto.cosmos.base.v1beta1 import coin_pb2 as cosmos_base_coin_pb
from .proto.cosmos.distribution.v1beta1 import tx_pb2 as tx_pb
from .proto.cosmos.staking.v1beta1 import tx_pb2 as cosmos_staking_tx_pb


class Composer:
    pricefeed = Pricefeed

    @staticmethod
    def coin(amount: float, denom: str):
        return cosmos_base_coin_pb.Coin(amount=str(amount), denom=denom)

    @staticmethod
    def msg_send(from_address: str, to_address: str, coins: List[cosmos_base_coin_pb.Coin]):
        return cosmos_bank_tx_pb.MsgSend(
            from_address=from_address,
            to_address=to_address,
            amount=coins,
        )

    @staticmethod
    def msg_exec(grantee: str, msgs: List):
        any_msgs: List[any_pb2.Any] = []
        for msg in msgs:
            any_msg = any_pb2.Any()
            any_msg.Pack(msg, type_url_prefix="")
            any_msgs.append(any_msg)

        return cosmos_authz_tx_pb.MsgExec(grantee=grantee, msgs=any_msgs)

    @staticmethod
    def msg_revoke(granter: str, grantee: str, msg_type: str):
        return cosmos_authz_tx_pb.MsgRevoke(granter=granter, grantee=grantee, msg_type_url=msg_type)

    @staticmethod
    def msg_delegate(delegator_address: str, validator_address: str, amount: float):
        return cosmos_staking_tx_pb.MsgDelegate(
            delegator_address=delegator_address,
            validator_address=validator_address,
            amount=Composer.coin(amount=amount, denom="inj"),
        )

    @staticmethod
    def msg_withdraw_delegator_reward(delegator_address: str, validator_address: str):

        return tx_pb.MsgWithdrawDelegatorReward(
            delegator_address=delegator_address, validator_address=validator_address
        )
