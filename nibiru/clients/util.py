from nibiru.utils import from_sdk_dec

BASE_ATTRS = [
    'ByteSize',
    'Clear',
    'ClearExtension',
    'ClearField',
    'CopyFrom',
    'DESCRIPTOR',
    'DiscardUnknownFields',
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
    '_InternalParse',
    '_InternalSerialize',
    '_Modified',
    '_SetListener',
    '_UpdateOneofState',
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
    '__weakref__',
    '_cached_byte_size',
    '_cached_byte_size_dirty',
    '_decoders_by_tag',
    '_extensions_by_name',
    '_extensions_by_number',
    '_fields',
    '_is_present_in_parent',
    '_listener',
    '_listener_for_children',
    '_oneofs',
    '_unknown_field_set',
    '_unknown_fields',
]


def deserialize(obj: object) -> dict:
    if isinstance(obj, (float, int, str)):
        return obj

    custom_dtypes = {
        str(field[1]): field[0].GetOptions().__getstate__().get("serialized", None)
        for field in obj.ListFields()
    }
    serialized_output = {}

    for attr in [field.name for field in obj._fields.keys()]:
        try:
            attr_search = obj.__getattribute__(attr)
        except AttributeError:
            continue

        custom_dtype = custom_dtypes.get(str(attr_search))

        if custom_dtype is not None:

            if "cosmos/cosmos-sdk/types.Dec" in str(custom_dtype):
                serialized_output[str(attr)] = from_sdk_dec(obj.__getattribute__(attr))

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
            print(attr)
            serialized_output[str(attr)] = deserialize(obj.__getattribute__(attr))

    return serialized_output
