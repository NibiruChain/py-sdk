from time import time
import json
from dataclasses import dataclass

from google.protobuf import any_pb2, message, timestamp_pb2

from nibiru.composers import ( 
    DexComposer, PerpComposer,
)

from .proto.cosmos.authz.v1beta1 import authz_pb2 as cosmos_authz_pb
from .proto.cosmos.authz.v1beta1 import tx_pb2 as cosmos_authz_tx_pb

from .proto.dex.v1 import tx_pb2 as dex_tx_pb
from .proto.dex.v1 import pool_pb2 as pool_tx_pb

from .proto.cosmos.bank.v1beta1 import tx_pb2 as cosmos_bank_tx_pb
from .proto.cosmos.base.v1beta1 import coin_pb2 as cosmos_base_coin_pb

from .proto.cosmos.staking.v1beta1 import tx_pb2 as cosmos_staking_tx_pb

from .proto.cosmos.distribution.v1beta1 import tx_pb2 as cosmos_distribution_tx_pb

from typing import List


@dataclass
class PoolAsset:
    token: cosmos_base_coin_pb.Coin
    weight: str


class Composer:
    def __init__(self, network: str):
        self.network = network
        self.dex = DexComposer()
        self.perp = PerpComposer()

    def Coin(self, amount: float, denom: str):
        return cosmos_base_coin_pb.Coin(amount=str(amount), denom=denom)

    def msg_send(self, from_address: str, to_address: str, amount: int, denom: str):
        return cosmos_bank_tx_pb.MsgSend(
            from_address=from_address,
            to_address=to_address,
            amount=[self.Coin(amount=amount, denom=denom)],
        )

    def msg_exec(self, grantee: str, msgs: List):
        any_msgs: List[any_pb2.Any] = []
        for msg in msgs:
            any_msg = any_pb2.Any()
            any_msg.Pack(msg, type_url_prefix="")
            any_msgs.append(any_msg)

        return cosmos_authz_tx_pb.MsgExec(grantee=grantee, msgs=any_msgs)

    def msg_revoke(self, granter: str, grantee: str, msg_type: str):
        return cosmos_authz_tx_pb.MsgRevoke(
            granter=granter, grantee=grantee, msg_type_url=msg_type
        )

    def msg_delegate(
        self,
        delegator_address: str,
        validator_address: str,
        amount: float
    ):

        be_amount = amount_to_backend(amount, 18)

        return cosmos_staking_tx_pb.MsgDelegate(
            delegator_address=delegator_address,
            validator_address=validator_address,
            amount=self.Coin(amount=be_amount, denom="inj"),
        )

    def msg_withdraw_delegator_reward(
        self,
        delegator_address: str,
        validator_address: str
    ):

        return cosmos_distribution_tx_pb.MsgWithdrawDelegatorReward(
            delegator_address=delegator_address,
            validator_address=validator_address
        )

    # # data field format: [request-msg-header][raw-byte-msg-response]
    # # you need to figure out this magic prefix number to trim request-msg-header off the data
    # # this method handles only exchange responses
    # @staticmethod
    # def MsgResponses(data, simulation=False):
    #     if not simulation:
    #         data = bytes.fromhex(data)
    #     header_map = {
    #         "/injective.exchange.v1beta1.MsgCreateSpotLimitOrder": injective_exchange_tx_pb.MsgCreateSpotLimitOrderResponse,
    #         "/injective.exchange.v1beta1.MsgCreateSpotMarketOrder": injective_exchange_tx_pb.MsgCreateSpotMarketOrderResponse,
    #         "/injective.exchange.v1beta1.MsgCreateDerivativeLimitOrder": injective_exchange_tx_pb.MsgCreateDerivativeLimitOrderResponse,
    #         "/injective.exchange.v1beta1.MsgCreateDerivativeMarketOrder": injective_exchange_tx_pb.MsgCreateDerivativeMarketOrderResponse,
    #         "/injective.exchange.v1beta1.MsgCancelSpotOrder": injective_exchange_tx_pb.MsgCancelSpotOrderResponse,
    #         "/injective.exchange.v1beta1.MsgCancelDerivativeOrder": injective_exchange_tx_pb.MsgCancelDerivativeOrderResponse,
    #         "/injective.exchange.v1beta1.MsgBatchCancelSpotOrders": injective_exchange_tx_pb.MsgBatchCancelSpotOrdersResponse,
    #         "/injective.exchange.v1beta1.MsgBatchCancelDerivativeOrders": injective_exchange_tx_pb.MsgBatchCancelDerivativeOrdersResponse,
    #         "/injective.exchange.v1beta1.MsgBatchCreateSpotLimitOrders": injective_exchange_tx_pb.MsgBatchCreateSpotLimitOrdersResponse,
    #         "/injective.exchange.v1beta1.MsgBatchCreateDerivativeLimitOrders": injective_exchange_tx_pb.MsgBatchCreateDerivativeLimitOrdersResponse,
    #         "/injective.exchange.v1beta1.MsgBatchUpdateOrders": injective_exchange_tx_pb.MsgBatchUpdateOrdersResponse,
    #         "/injective.exchange.v1beta1.MsgDeposit": injective_exchange_tx_pb.MsgDepositResponse,
    #         "/injective.exchange.v1beta1.MsgWithdraw": injective_exchange_tx_pb.MsgWithdrawResponse,
    #         "/injective.exchange.v1beta1.MsgSubaccountTransfer": injective_exchange_tx_pb.MsgSubaccountTransferResponse,
    #         "/injective.exchange.v1beta1.MsgLiquidatePosition": injective_exchange_tx_pb.MsgLiquidatePositionResponse,
    #         "/injective.exchange.v1beta1.MsgIncreasePositionMargin": injective_exchange_tx_pb.MsgIncreasePositionMarginResponse,
    #         "/injective.auction.v1beta1.MsgBid": injective_auction_tx_pb.MsgBidResponse,
    #         "/injective.exchange.v1beta1.MsgCreateBinaryOptionsLimitOrder": injective_exchange_tx_pb.MsgCreateBinaryOptionsLimitOrderResponse,
    #         "/injective.exchange.v1beta1.MsgCreateBinaryOptionsMarketOrder": injective_exchange_tx_pb.MsgCreateBinaryOptionsMarketOrderResponse,
    #         "/injective.exchange.v1beta1.MsgCancelBinaryOptionsOrder": injective_exchange_tx_pb.MsgCancelBinaryOptionsOrderResponse,
    #         "/injective.exchange.v1beta1.MsgAdminUpdateBinaryOptionsMarket": injective_exchange_tx_pb.MsgAdminUpdateBinaryOptionsMarketResponse,
    #         "/injective.exchange.v1beta1.MsgInstantBinaryOptionsMarketLaunch": injective_exchange_tx_pb.MsgInstantBinaryOptionsMarketLaunchResponse,
    #         "/cosmos.bank.v1beta1.MsgSend": cosmos_bank_tx_pb.MsgSendResponse,
    #         "/cosmos.authz.v1beta1.MsgGrant": cosmos_authz_tx_pb.MsgGrantResponse,
    #         "/cosmos.authz.v1beta1.MsgExec": cosmos_authz_tx_pb.MsgExecResponse,
    #         "/cosmos.authz.v1beta1.MsgRevoke": cosmos_authz_tx_pb.MsgRevokeResponse,
    #         "/injective.oracle.v1beta1.MsgRelayPriceFeedPrice": injective_oracle_tx_pb.MsgRelayPriceFeedPriceResponse,
    #         "/injective.oracle.v1beta1.MsgRelayProviderPrices": injective_oracle_tx_pb.MsgRelayProviderPrices
    #     }

    #     response = tx_response_pb.TxResponseData.FromString(data)
    #     msgs = []
    #     for msg in response.messages:
    #         msgs.append(header_map[msg.header].FromString(msg.data))

    #     return msgs

    # @staticmethod
    # def UnpackMsgExecResponse(msg_type, data):
    #     header_map = {
    #         "MsgCreateSpotLimitOrder": injective_exchange_tx_pb.MsgCreateSpotLimitOrderResponse,
    #         "MsgCreateSpotMarketOrder": injective_exchange_tx_pb.MsgCreateSpotMarketOrderResponse,
    #         "MsgCreateDerivativeLimitOrder": injective_exchange_tx_pb.MsgCreateDerivativeLimitOrderResponse,
    #         "MsgCreateDerivativeMarketOrder": injective_exchange_tx_pb.MsgCreateDerivativeMarketOrderResponse,
    #         "MsgCancelSpotOrder": injective_exchange_tx_pb.MsgCancelSpotOrderResponse,
    #         "MsgCancelDerivativeOrder": injective_exchange_tx_pb.MsgCancelDerivativeOrderResponse,
    #         "MsgBatchCancelSpotOrders": injective_exchange_tx_pb.MsgBatchCancelSpotOrdersResponse,
    #         "MsgBatchCancelDerivativeOrders": injective_exchange_tx_pb.MsgBatchCancelDerivativeOrdersResponse,
    #         "MsgBatchCreateSpotLimitOrders": injective_exchange_tx_pb.MsgBatchCreateSpotLimitOrdersResponse,
    #         "MsgBatchCreateDerivativeLimitOrders": injective_exchange_tx_pb.MsgBatchCreateDerivativeLimitOrdersResponse,
    #         "MsgBatchUpdateOrders": injective_exchange_tx_pb.MsgBatchUpdateOrdersResponse,
    #         "MsgDeposit": injective_exchange_tx_pb.MsgDepositResponse,
    #         "MsgWithdraw": injective_exchange_tx_pb.MsgWithdrawResponse,
    #         "MsgSubaccountTransfer": injective_exchange_tx_pb.MsgSubaccountTransferResponse,
    #         "MsgLiquidatePosition": injective_exchange_tx_pb.MsgLiquidatePositionResponse,
    #         "MsgIncreasePositionMargin": injective_exchange_tx_pb.MsgIncreasePositionMarginResponse,
    #         "MsgCreateBinaryOptionsLimitOrder": injective_exchange_tx_pb.MsgCreateBinaryOptionsLimitOrderResponse,
    #         "MsgCreateBinaryOptionsMarketOrder": injective_exchange_tx_pb.MsgCreateBinaryOptionsMarketOrderResponse,
    #         "MsgCancelBinaryOptionsOrder": injective_exchange_tx_pb.MsgCancelBinaryOptionsOrderResponse,
    #         "MsgAdminUpdateBinaryOptionsMarket": injective_exchange_tx_pb.MsgAdminUpdateBinaryOptionsMarketResponse,
    #         "MsgInstantBinaryOptionsMarketLaunch": injective_exchange_tx_pb.MsgInstantBinaryOptionsMarketLaunchResponse
    #     }

    #     return header_map[msg_type].FromString(bytes(data, "utf-8"))
