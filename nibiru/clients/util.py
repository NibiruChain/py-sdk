from nibiru.utils import sdkdec_to_float, sdkint_to_float

BASE_ATTRS = [
    'ByteSize',
    'Clear',
    'ClearExtension',
    'ClearField',
    'CopyFrom',
    'DESCRIPTOR',
    'DiscardUnknownFields',
    'Extensions',
    'FindInitializationErrors',
    'FromString',
    'HasExtension',
    'HasField',
    'IsInitialized',
    'ListFields',
    'MergeFrom',
    'MergeFromString',
    'ParseFromString',
    'RegisterExtension',
    'SerializePartialToString',
    'SerializeToString',
    'SetInParent',
    'UnknownFields',
    'WhichOneof',
    '_CheckCalledFromGeneratedFile',
    '_SetListener',
    '__class__',
    '__deepcopy__',
    '__delattr__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__getstate__',
    '__gt__',
    '__hash__',
    '__init__',
    '__init_subclass__',
    '__le__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__setattr__',
    '__setstate__',
    '__sizeof__',
    '__slots__',
    '__str__',
    '__subclasshook__',
    '__unicode__',
    '_extensions_by_name',
    '_extensions_by_number',
]


def deserialize(obj: object) -> dict:
    custom_dtypes = {
        str(field[1]): field[0].GetOptions().__getstate__().get("serialized", None) for field in obj.ListFields()
    }

    serialized_output = {}

    for attr in dir(obj):
        if attr not in BASE_ATTRS:

            attr_search = obj.__getattribute__(attr)

            custom_dtype = custom_dtypes.get(str(attr_search))

            if custom_dtype is not None:

                if "cosmos/cosmos-sdk/types.Dec" in str(custom_dtype):
                    serialized_output[str(attr)] = sdkdec_to_float(obj.__getattribute__(attr))

                elif "cosmos/cosmos-sdk/types.Int" in str(custom_dtype):
                    serialized_output[str(attr)] = sdkint_to_float(obj.__getattribute__(attr))
                else:
                    try:
                        val = obj.__getattribute__(attr)
                        if hasattr(val, '__len__') and not isinstance(val, str):
                            updated_vals = []
                            for v in val:
                                updated_vals.append(deserialize(v))
                            serialized_output[str(attr)] = updated_vals
                        else:
                            serialized_output[str(attr)] = deserialize(val)
                    except:
                        serialized_output[str(attr)] = obj.__getattribute__(attr)
            else:
                serialized_output[str(attr)] = deserialize(obj.__getattribute__(attr))

    return serialized_output
