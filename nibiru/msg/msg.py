import dataclasses

from nibiru.msg.bank import MsgsBank
from nibiru.msg.perp import MsgsPerp
from nibiru.msg.spot import MsgsSpot
from nibiru.msg.staking import MsgsStaking


@dataclasses.dataclass
class MsgClient:
    """
    The 'MsgClient' exposes all available messages in the Nibiru Chain Python SDK.
    The class attributes of the client separate these messages by module.

    Attributes:
        bank: Methods for the Cosmos x/bank module.
        spot: Methods for the Nibiru Chain x/spot module.
        perp: Methods for the Nibiru Chain x/perp module
        staking: Methods for the Cosmos x/staking and x/distribution modules.
    """

    bank = MsgsBank
    spot = MsgsSpot
    perp = MsgsPerp
    staking = MsgsStaking


Msg = MsgClient()
