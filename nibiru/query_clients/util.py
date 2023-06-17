import importlib
from typing import List, Optional, Union

import grpc
import grpc._channel
from google.protobuf import message
from grpc import Channel
from nibiru_proto.proto.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest
from nibiru_proto.proto.cosmos.tx.v1beta1.tx_pb2 import Tx
from nibiru_proto.proto.tendermint.types.block_pb2 import Block
from nibiru_proto.proto.util.v1 import query_pb2 as util_type
from nibiru_proto.proto.util.v1 import query_pb2_grpc as util_query

from nibiru import utils
from nibiru.exceptions import QueryError


def message_to_dict(pb_msg: message.Message) -> dict:
    """Converts a proto message into a dictionary.

    - sdk.Dec values are converted to floats.
    - sdk.Int values are converted to ints.
    - Missing fields become blank strings.

    Args:
        pb_msg (protobuf.message.Message)

    Returns:
        dict: 'pb_msg' as a JSON-able dictionary.
    """
    if not isinstance(pb_msg, message.Message):
        return pb_msg

    custom_types = {}  # map of field name to custom type
    for field in pb_msg.ListFields():
        field_options = field[0].GetOptions()
        for field_option in field_options.ListFields():
            if field_option[0].name == "customtype":
                custom_types[field[0].name] = field_option[1]

    output = {}

    for attr_name in pb_msg.DESCRIPTOR.fields_by_name.keys():
        custom_type = custom_types.get(attr_name)
        val = getattr(pb_msg, attr_name)

        if custom_type == "github.com/cosmos/cosmos-sdk/types.Dec":
            output[str(attr_name)] = utils.from_sdk_dec(val)
        elif custom_type == "github.com/cosmos/cosmos-sdk/types.Int":
            output[str(attr_name)] = utils.from_sdk_int(val)
        elif hasattr(val, '__len__') and not isinstance(val, str):
            output[str(attr_name)] = [message_to_dict(v) for v in val]
        else:
            output[str(attr_name)] = message_to_dict(val)

    return output


class QueryClient:
    def query(
        self,
        api_callable: grpc.UnaryUnaryMultiCallable,
        req: message.Message,
        should_deserialize: bool = True,
        height: Optional[int] = None,
    ) -> Union[dict, message.Message]:
        try:
            output: message.Message = api_callable(
                req,
                **(
                    {"metadata": (('x-cosmos-block-height', str(height)),)}
                    if height
                    else {}
                ),
            )
            if should_deserialize:
                return message_to_dict(output)
            return output
        except grpc._channel._InactiveRpcError as err:
            raise QueryError(
                f"Error on {str(api_callable._method).split('/')[-1][:-1]}: {err._state.details}"
            ) from None


def get_page_request(kwargs) -> PageRequest:
    return PageRequest(
        key=kwargs.get("key"),
        offset=kwargs.get("offset"),
        limit=kwargs.get("limit"),
        count_total=kwargs.get("count_total"),
        reverse=kwargs.get("reverse"),
    )


def get_msg_pb_by_type_url(type_url: str) -> Optional[message.Message]:
    """
    Tries loading protobuf class by type url.
    Examples type urls:
        /cosmos.bank.v1beta1.MsgSend
        /nibiru.perp.v1.MsgOpenPosition
    """
    class_ = None
    try:
        type_url = type_url.replace("/", "")
        module_name, class_name = type_url.rsplit(".", 1)
        if module_name.startswith("nibiru."):
            module_name = module_name.split(".", 1)[1]
        module_name = f"nibiru_proto.proto.{module_name}.tx_pb2"
        module_ = importlib.import_module(module_name)
        class_ = getattr(module_, class_name)()
    except Exception:
        pass

    return class_ or None


def get_block_messages(block: Block) -> List[dict]:
    """
    Rerurns block messages as a list of dicts.
    Matches corresponding messages types by type_url.
    """
    messages = []
    for tx in block.data.txs:
        tx_pb = Tx()
        tx_pb.MergeFromString(tx)

        for msg in tx_pb.body.messages:
            msg_pb: message.Message = get_msg_pb_by_type_url(msg.type_url)
            if msg_pb:
                msg_pb.ParseFromString(msg.value)
                messages.append(
                    {"type_url": msg.type_url, "value": message_to_dict(msg_pb)}
                )
    return messages


class UtilQueryClient(QueryClient):
    """
    UtilQueryClient allows to query the endpoints made available by the util
    module of Nibiru Chain.
    """

    def __init__(self, channel: Channel):
        self.api = util_query.QueryStub(channel)

    def module_accounts(self) -> dict:
        """
        Returns information module accounts like perp, vault etc.
        Includes account name, address and balances.

        Example Return Value:

        ```json
        {
          "accounts": [
            {
              "name": "perp",
              "address": "nibi1sr9a7yav4nu9n335atnkwgpcwz7s3p8puwaxgq",
              "balance": []
            },
            {
              "name": "vault",
              "address": "nibi1umc2r7a58jy3jmw0e0hctyy0rx45chmurptawl",
              "balance": []
            }
          ]
        }
        ```
        """
        return self.query(
            api_callable=self.api.ModuleAccounts,
            req=util_type.QueryModuleAccountsRequest(),
            should_deserialize=True,
        )
