class NibiruError(Exception):
    pass


class SimulationError(NibiruError):
    pass


class TxError(NibiruError):
    pass


class ErrorQueryTx(NibiruError):
    """Expresses failure to to query a tx with its hash."""


class QueryError(NibiruError):
    pass
