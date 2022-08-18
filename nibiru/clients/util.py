from google.protobuf.json_format import MessageToDict

from nibiru.utils import from_sdk_dec


def camel_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')


def t_dict(d):
    if isinstance(d, list):
        return [t_dict(i) if isinstance(i, (dict, list)) else i for i in d]
    return {
        camel_to_snake(a): t_dict(b) if isinstance(b, (dict, list)) else b
        for a, b in d.items()
    }


def deserialize(proto_message: object) -> dict:
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
                output[field.camelcase_name] = deserialize(
                    proto_message.__getattribute__(field.camelcase_name)
                )
            except AttributeError:
                output[field.camelcase_name] = output[field.camelcase_name]

        elif is_sdk_dec[field.camelcase_name]:
            output[field.camelcase_name] = from_sdk_dec(output[field.camelcase_name])

    return t_dict(output)
