from typing import Dict, List

from google.protobuf import message as protobuf_message
from google.protobuf.json_format import MessageToDict

from nibiru.utils import from_sdk_dec, from_sdk_int

BASE_ATTRS = (
    ["ByteSize", "Clear", "ClearExtension", "ClearField", "CopyFrom", "DESCRIPTOR"]
    + ["DiscardUnknownFields", "Extensions", "FindInitializationErrors", "FromString"]
    + [
        "HasExtension",
        "HasField",
        "IsInitialized",
        "ListFields",
        "MergeFrom",
    ]
    + ["MergeFromString", "ParseFromString", "RegisterExtension"]
    + ["SerializePartialToString", "SerializeToString", "SetInParent"]
    + ["UnknownFields", "WhichOneof", "_CheckCalledFromGeneratedFile", "_SetListener"]
    + ["__class__", "__deepcopy__", "__delattr__", "__dir__", "__doc__"]
    + ["__eq__", "__format__", "__ge__", "__getattribute__", "__getstate__"]
    + ["__gt__", "__hash__", "__init__", "__init_subclass__", "__le__", "__lt__"]
    + ["__module__", "__ne__", "__new__", "__reduce__", "__reduce_ex__", "__repr__"]
    + ["__setattr__", "__setstate__", "__sizeof__", "__slots__", "__str__"]
    + ["__subclasshook__", "__unicode__", "_extensions_by_name"]
    + ["_extensions_by_number"]
)


def camel_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')


def t_dict(d):
    if isinstance(d, list):
        return [t_dict(i) if isinstance(i, (dict, list)) else i for i in d]
    return {
        camel_to_snake(a): t_dict(b) if isinstance(b, (dict, list)) else b
        for a, b in d.items()
    }


def deserialize(pb_msg: protobuf_message.Message) -> dict:
    custom_dtypes: Dict[str, bytes] = {
        str(field[1]): field[0].GetOptions().__getstate__().get("serialized", None)
        for field in pb_msg.ListFields()
    }
    serialized_output = {}
    expected_fields: List[str] = [
        attr for attr in dir(pb_msg) if attr not in BASE_ATTRS
    ]

    for _, attr in enumerate(expected_fields):

        attr_search = pb_msg.__getattribute__(attr)
        custom_dtype = custom_dtypes.get(str(attr_search))

        if custom_dtype is not None:

            if "sdk/types.Dec" in str(custom_dtype):
                serialized_output[str(attr)] = from_sdk_dec(
                    pb_msg.__getattribute__(attr)
                )
            elif "sdk/types.Int" in str(custom_dtype):
                serialized_output[str(attr)] = from_sdk_int(
                    pb_msg.__getattribute__(attr)
                )
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


def deserialize_exp(proto_message: object) -> dict:
    """
    Take a proto message and convert it into a dictionnary.
    sdk.Dec values are converted to be consistent with txs.

    Args:
        proto_message (object): The proto message

    Returns:
        dict: The dictionary
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

    return t_dict(output)
