class NibiruError(Exception):
    pass


class ValueTooLargeError(NibiruError):
    pass


class EmptyMsgError(NibiruError):
    pass


class NotFoundError(NibiruError):
    pass


class UndefinedError(NibiruError):
    pass


class DecodeError(NibiruError):
    pass


class ConvertError(NibiruError):
    pass


class SchemaError(NibiruError):
    pass


class SimulationError(NibiruError):
    pass


class TxError(NibiruError):
    pass


class InvalidArgumentError(NibiruError):
    pass
