class NibiruError(Exception):
    pass


class SimulationError(NibiruError):
    pass


class TxError(NibiruError):
    pass


class QueryError(NibiruError):
    pass
