import importlib
from typing import Dict, List, Optional, Union

import grpc
import grpc._channel
from google.protobuf import json_format, message
from grpc import Channel
from nibiru_proto.proto.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest
from nibiru_proto.proto.cosmos.tx.v1beta1.tx_pb2 import Tx
from nibiru_proto.proto.tendermint.types.block_pb2 import Block
from nibiru_proto.proto.util.v1 import query_pb2 as util_type
from nibiru_proto.proto.util.v1 import query_pb2_grpc as util_query

from nibiru import utils
from nibiru.exceptions import QueryError

PROTOBUF_MSG_BASE_ATTRS: List[str] = (
    dir(message.Message)
    + ['Extensions', 'FindInitializationErrors', '_CheckCalledFromGeneratedFile']
    + ['_extensions_by_name', '_extensions_by_number']
)
"""PROTOBUF_MSG_BASE_ATTRS (List[str]): The default attributes and methods of
an instance of the 'protobuf.message.Message' class.
"""


def camel_to_snake(camel: str):
    return ''.join(
        ['_' + char.lower() if char.isupper() else char for char in camel]
    ).lstrip('_')


def dict_keys_from_camel_to_snake(d):
    """
    Transform all keys from the dictionnary from camelcase to snake case.

    Args:
        d (dict): The dictionary to transform

    Returns:
        dict: The dictionary transformed
    """
    if isinstance(d, list):
        return [
            dict_keys_from_camel_to_snake(i) if isinstance(i, (dict, list)) else i
            for i in d
        ]
    return {
        camel_to_snake(a): dict_keys_from_camel_to_snake(b)
        if isinstance(b, (dict, list))
        else b
        for a, b in d.items()
    }


def deserialize(pb_msg: message.Message, no_sdk_transformation: bool = False) -> dict:
    """Deserializes a proto message into a dictionary.

    - sdk.Dec values are converted to floats.
    - sdk.Int values are converted to ints.
    - Missing fields become blank strings.

    Args:
        pb_msg (protobuf.message.Message)
        no_sdk_transformation (bool): Wether to bypass the sdk transformation. Default to False

    Returns:
        dict: 'pb_msg' as a JSON-able dictionary.
    """
    if not isinstance(pb_msg, message.Message):
        return pb_msg
    custom_dtypes: Dict[str, bytes] = {
        str(field[1]): field[0].GetOptions().__getstate__().get("serialized", None)
        for field in pb_msg.ListFields()
    }
    serialized_output = {}
    expected_fields: List[str] = list(pb_msg.DESCRIPTOR.fields_by_name.keys())

    for _, attr in enumerate(expected_fields):
        attr_search = pb_msg.__getattribute__(attr)
        custom_dtype = custom_dtypes.get(str(attr_search))

        if custom_dtype is not None:
            if "sdk/types.Dec" in str(custom_dtype):
                if no_sdk_transformation:
                    serialized_output[str(attr)] = float(pb_msg.__getattribute__(attr))
                else:
                    serialized_output[str(attr)] = utils.from_sdk_dec(
                        pb_msg.__getattribute__(attr)
                    )
            elif "sdk/types.Int" in str(custom_dtype):
                if no_sdk_transformation:
                    serialized_output[str(attr)] = int(pb_msg.__getattribute__(attr))
                else:
                    serialized_output[str(attr)] = utils.from_sdk_int(
                        pb_msg.__getattribute__(attr)
                    )
            elif "Int" in str(custom_dtype):  # Used for sdk.Coin message normalization
                serialized_output[str(attr)] = int(pb_msg.__getattribute__(attr))
            else:
                val = pb_msg.__getattribute__(attr)
                if hasattr(val, '__len__') and not isinstance(val, str):
                    updated_vals = []
                    for v in val:
                        updated_vals.append(deserialize(v))
                    serialized_output[str(attr)] = updated_vals
                else:
                    serialized_output[str(attr)] = deserialize(val)
        elif custom_dtype is None and not attr_search:
            if str(attr_search) == "[]":
                serialized_output[str(attr)] = []
            else:
                serialized_output[str(attr)] = attr_search
        else:
            serialized_output[str(attr)] = deserialize(pb_msg.__getattribute__(attr))

    return serialized_output


def deserialize_exp(proto_message: message.Message) -> dict:
    """
    Take a proto message and convert it into a dictionnary.
    sdk.Dec values are converted to be consistent with txs.

    Args:
        proto_message (protobuf.message.Message)

    Returns:
        dict
    """
    output = json_format.MessageToDict(proto_message)

    is_sdk_dec = {
        field.camelcase_name: "types.Dec" in str(field.GetOptions())
        for field in proto_message.DESCRIPTOR.fields
    }

    for field in proto_message.DESCRIPTOR.fields:
        if field.message_type is not None:
            # This is another proto object
            try:
                output[field.camelcase_name] = deserialize_exp(
                    proto_message.__getattribute__(field.camelcase_name)
                )
            except AttributeError:
                output[field.camelcase_name] = output[field.camelcase_name]

        elif is_sdk_dec[field.camelcase_name]:
            output[field.camelcase_name] = utils.from_sdk_dec(
                output[field.camelcase_name]
            )

    return dict_keys_from_camel_to_snake(output)


class QueryClient:
    def query(
        self,
        api_callable: grpc.UnaryUnaryMultiCallable,
        req: message.Message,
        should_deserialize: bool = True,
    ) -> Union[dict, message.Message]:
        try:
            output: message.Message = api_callable(req)
            if should_deserialize:
                return deserialize(output)
            return output
        except grpc._channel._InactiveRpcError as err:
            raise QueryError(
                f"Error on {str(api_callable._method).split('/')[-1][:-1]}: {err._state.details}"
            ) from None


def get_page_request(kwargs):
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
                    {"type_url": msg.type_url, "value": deserialize(msg_pb)}
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
