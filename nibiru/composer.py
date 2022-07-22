from typing import List

from google.protobuf import any_pb2

from .composers import Dex, Perp, Pricefeed
from .proto.cosmos.authz.v1beta1 import tx_pb2 as cosmos_authz_tx_pb
from .proto.cosmos.bank.v1beta1 import tx_pb2 as cosmos_bank_tx_pb
from .proto.cosmos.base.v1beta1 import coin_pb2 as cosmos_base_coin_pb
from .proto.cosmos.distribution.v1beta1 import tx_pb2 as tx_pb
from .proto.cosmos.staking.v1beta1 import tx_pb2 as cosmos_staking_tx_pb


class Composer:
    dex = Dex
    perp = Perp
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

    # # data field format: [request-msg-header][raw-byte-msg-response]
    # # you need to figure out this magic prefix number to trim request-msg-header off the data
    # # this method handles only exchange responses
    # @staticmethod
    # def MsgResponses(data, simulation=False):
    #     if not simulation:
    #         data = bytes.fromhex(data)
    #     header_map = {
    #         "/nibiru.exchange.v1beta1.MsgCreateSpotLimitOrder": injective_exchange_tx_pb.MsgCreateSpotLimitOrderResponse,
    #         "/nibiru.exchange.v1beta1.MsgCreateSpotMarketOrder": injective_exchange_tx_pb.MsgCreateSpotMarketOrderResponse,
    #         "/nibiru.exchange.v1beta1.MsgCreateDerivativeLimitOrder": injective_exchange_tx_pb.MsgCreateDerivativeLimitOrderResponse,
    #         "/nibiru.exchange.v1beta1.MsgCreateDerivativeMarketOrder": injective_exchange_tx_pb.MsgCreateDerivativeMarketOrderResponse,
    #         "/nibiru.exchange.v1beta1.MsgCancelSpotOrder": injective_exchange_tx_pb.MsgCancelSpotOrderResponse,
    #         "/nibiru.exchange.v1beta1.MsgCancelDerivativeOrder": injective_exchange_tx_pb.MsgCancelDerivativeOrderResponse,
    #         "/nibiru.exchange.v1beta1.MsgBatchCancelSpotOrders": injective_exchange_tx_pb.MsgBatchCancelSpotOrdersResponse,
    #         "/nibiru.exchange.v1beta1.MsgBatchCancelDerivativeOrders": injective_exchange_tx_pb.MsgBatchCancelDerivativeOrdersResponse,
    #         "/nibiru.exchange.v1beta1.MsgBatchCreateSpotLimitOrders": injective_exchange_tx_pb.MsgBatchCreateSpotLimitOrdersResponse,
    #         "/nibiru.exchange.v1beta1.MsgBatchCreateDerivativeLimitOrders": injective_exchange_tx_pb.MsgBatchCreateDerivativeLimitOrdersResponse,
    #         "/nibiru.exchange.v1beta1.MsgBatchUpdateOrders": injective_exchange_tx_pb.MsgBatchUpdateOrdersResponse,
    #         "/nibiru.exchange.v1beta1.MsgDeposit": injective_exchange_tx_pb.MsgDepositResponse,
    #         "/nibiru.exchange.v1beta1.MsgWithdraw": injective_exchange_tx_pb.MsgWithdrawResponse,
    #         "/nibiru.exchange.v1beta1.MsgSubaccountTransfer": injective_exchange_tx_pb.MsgSubaccountTransferResponse,
    #         "/nibiru.exchange.v1beta1.MsgLiquidatePosition": injective_exchange_tx_pb.MsgLiquidatePositionResponse,
    #         "/nibiru.exchange.v1beta1.MsgIncreasePositionMargin": injective_exchange_tx_pb.MsgIncreasePositionMarginResponse,
    #         "/nibiru.auction.v1beta1.MsgBid": injective_auction_tx_pb.MsgBidResponse,
    #         "/nibiru.exchange.v1beta1.MsgCreateBinaryOptionsLimitOrder": injective_exchange_tx_pb.MsgCreateBinaryOptionsLimitOrderResponse,
    #         "/nibiru.exchange.v1beta1.MsgCreateBinaryOptionsMarketOrder": injective_exchange_tx_pb.MsgCreateBinaryOptionsMarketOrderResponse,
    #         "/nibiru.exchange.v1beta1.MsgCancelBinaryOptionsOrder": injective_exchange_tx_pb.MsgCancelBinaryOptionsOrderResponse,
    #         "/nibiru.exchange.v1beta1.MsgAdminUpdateBinaryOptionsMarket": injective_exchange_tx_pb.MsgAdminUpdateBinaryOptionsMarketResponse,
    #         "/nibiru.exchange.v1beta1.MsgInstantBinaryOptionsMarketLaunch": injective_exchange_tx_pb.MsgInstantBinaryOptionsMarketLaunchResponse,
    #         "/cosmos.bank.v1beta1.MsgSend": cosmos_bank_tx_pb.MsgSendResponse,
    #         "/cosmos.authz.v1beta1.MsgGrant": cosmos_authz_tx_pb.MsgGrantResponse,
    #         "/cosmos.authz.v1beta1.MsgExec": cosmos_authz_tx_pb.MsgExecResponse,
    #         "/cosmos.authz.v1beta1.MsgRevoke": cosmos_authz_tx_pb.MsgRevokeResponse,
    #         "/nibiru.oracle.v1beta1.MsgRelayPriceFeedPrice": injective_oracle_tx_pb.MsgRelayPriceFeedPriceResponse,
    #         "/nibiru.oracle.v1beta1.MsgRelayProviderPrices": injective_oracle_tx_pb.MsgRelayProviderPrices
    #     }

    #     response = tx_response_pb.TxResponseData.FromString(data)
    #     msgs = []
    #     for msg in response.messages:
    #         msgs.append(header_map[msg.header].FromString(msg.data))

    #     return msgs

    # @staticmethod
    # def UnpackMsgExecResponse(msg_type, data):
    #     header_map = {
    #         "MsgCreateSpotLimitOrder": nibiru_exchange_tx_pb.MsgCreateSpotLimitOrderResponse,
    #         "MsgCreateSpotMarketOrder": nibiru_exchange_tx_pb.MsgCreateSpotMarketOrderResponse,
    #         "MsgCreateDerivativeLimitOrder": nibiru_exchange_tx_pb.MsgCreateDerivativeLimitOrderResponse,
    #         "MsgCreateDerivativeMarketOrder": nibiru_exchange_tx_pb.MsgCreateDerivativeMarketOrderResponse,
    #         "MsgCancelSpotOrder": nibiru_exchange_tx_pb.MsgCancelSpotOrderResponse,
    #         "MsgCancelDerivativeOrder": nibiru_exchange_tx_pb.MsgCancelDerivativeOrderResponse,
    #         "MsgBatchCancelSpotOrders": nibiru_exchange_tx_pb.MsgBatchCancelSpotOrdersResponse,
    #         "MsgBatchCancelDerivativeOrders": nibiru_exchange_tx_pb.MsgBatchCancelDerivativeOrdersResponse,
    #         "MsgBatchCreateSpotLimitOrders": nibiru_exchange_tx_pb.MsgBatchCreateSpotLimitOrdersResponse,
    #         "MsgBatchCreateDerivativeLimitOrders": nibiru_exchange_tx_pb.MsgBatchCreateDerivativeLimitOrdersResponse,
    #         "MsgBatchUpdateOrders": nibiru_exchange_tx_pb.MsgBatchUpdateOrdersResponse,
    #         "MsgDeposit": nibiru_exchange_tx_pb.MsgDepositResponse,
    #         "MsgWithdraw": nibiru_exchange_tx_pb.MsgWithdrawResponse,
    #         "MsgSubaccountTransfer": nibiru_exchange_tx_pb.MsgSubaccountTransferResponse,
    #         "MsgLiquidatePosition": nibiru_exchange_tx_pb.MsgLiquidatePositionResponse,
    #         "MsgIncreasePositionMargin": nibiru_exchange_tx_pb.MsgIncreasePositionMarginResponse,
    #         "MsgCreateBinaryOptionsLimitOrder": nibiru_exchange_tx_pb.MsgCreateBinaryOptionsLimitOrderResponse,
    #         "MsgCreateBinaryOptionsMarketOrder": nibiru_exchange_tx_pb.MsgCreateBinaryOptionsMarketOrderResponse,
    #         "MsgCancelBinaryOptionsOrder": nibiru_exchange_tx_pb.MsgCancelBinaryOptionsOrderResponse,
    #         "MsgAdminUpdateBinaryOptionsMarket": nibiru_exchange_tx_pb.MsgAdminUpdateBinaryOptionsMarketResponse,
    #         "MsgInstantBinaryOptionsMarketLaunch": nibiru_exchange_tx_pb.MsgInstantBinaryOptionsMarketLaunchResponse
    #     }

    #     return header_map[msg_type].FromString(bytes(data, "utf-8"))
