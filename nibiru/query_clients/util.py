from typing import Dict, List, Union

import google.protobuf.message
from google.protobuf import message as protobuf_message
from google.protobuf.json_format import MessageToDict
from grpc import UnaryUnaryMultiCallable
from grpc._channel import _InactiveRpcError

from nibiru.exceptions import QueryError
from nibiru.utils import from_sdk_dec, from_sdk_int

PROTOBUF_MSG_BASE_ATTRS: List[str] = (
    dir(protobuf_message.Message)
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


def deserialize(
    pb_msg: protobuf_message.Message, no_sdk_transformation: bool = False
) -> dict:
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
    if not isinstance(pb_msg, protobuf_message.Message):
        raise TypeError(f"expted protobuf Message for 'pb_msg', not {type(pb_msg)}")
    custom_dtypes: Dict[str, bytes] = {
        str(field[1]): field[0].GetOptions().__getstate__().get("serialized", None)
        for field in pb_msg.ListFields()
    }
    serialized_output = {}
    expected_fields: List[str] = [
        attr for attr in dir(pb_msg) if attr not in PROTOBUF_MSG_BASE_ATTRS
    ]

    for _, attr in enumerate(expected_fields):

        attr_search = pb_msg.__getattribute__(attr)
        custom_dtype = custom_dtypes.get(str(attr_search))

        if custom_dtype is not None:

            if "sdk/types.Dec" in str(custom_dtype):
                if no_sdk_transformation:
                    serialized_output[str(attr)] = float(pb_msg.__getattribute__(attr))
                else:
                    serialized_output[str(attr)] = from_sdk_dec(
                        pb_msg.__getattribute__(attr)
                    )
            elif "sdk/types.Int" in str(custom_dtype):
                if no_sdk_transformation:
                    serialized_output[str(attr)] = int(pb_msg.__getattribute__(attr))
                else:
                    serialized_output[str(attr)] = from_sdk_int(
                        pb_msg.__getattribute__(attr)
                    )
            elif "Int" in str(custom_dtype):  # Used for sdk.Coin message normalization
                serialized_output[str(attr)] = int(pb_msg.__getattribute__(attr))
            else:
                try:
                    val = pb_msg.__getattribute__(attr)
                    if hasattr(val, '__len__') and not isinstance(val, str):
                        updated_vals = []
                        for v in val:
                            updated_vals.append(deserialize(v))
                        serialized_output[str(attr)] = updated_vals
                    else:
                        serialized_output[str(attr)] = deserialize(val)
                except:
                    serialized_output[str(attr)] = pb_msg.__getattribute__(attr)
        elif (custom_dtype is None) and (attr_search == ''):
            serialized_output[str(attr)] = ""
        else:
            serialized_output[str(attr)] = deserialize(pb_msg.__getattribute__(attr))

    return serialized_output


def deserialize_exp(proto_message: protobuf_message.Message) -> dict:
    """
    Take a proto message and convert it into a dictionnary.
    sdk.Dec values are converted to be consistent with txs.

    Args:
        proto_message (protobuf.message.Message)

    Returns:
        dict
    """
    output = MessageToDict(proto_message)

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
            output[field.camelcase_name] = from_sdk_dec(output[field.camelcase_name])

    return dict_keys_from_camel_to_snake(output)


class QueryClient:
    def query(
        self,
        api_callable: UnaryUnaryMultiCallable,
        req: google.protobuf.message.Message,
        should_deserialize: bool = True,
    ) -> Union[dict, google.protobuf.message.Message]:

        try:
            output: google.protobuf.message.Message = api_callable(req)
            if should_deserialize:
                return deserialize(output)
            return output
        except _InactiveRpcError as err:
            raise QueryError(
                f"Error on {str(api_callable._method).split('/')[-1][:-1]}: {err._state.details}"
            ) from None
