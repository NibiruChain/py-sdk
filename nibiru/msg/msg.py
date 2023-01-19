import dataclasses

from nibiru.msg.bank import MsgsBank
from nibiru.msg.dex import MsgsDex
from nibiru.msg.perp import MsgsPerp
from nibiru.msg.staking import MsgsStaking


@dataclasses.dataclass
class MsgClient:
    """
    The 'MsgClient' exposes all available messages in the Nibiru Chain Python SDK.
    The class attributes of the client separate these messages by module.

    Attributes:
        bank: Methods for the Cosmos x/bank module.
        dex: Methods for the Nibiru Chain x/dex module.
        perp: Methods for the Nibiru Chain x/perp module
        staking: Methods for the Cosmos x/staking and x/distribution modules.
    """

    bank = MsgsBank
    dex = MsgsDex
    perp = MsgsPerp
    staking = MsgsStaking


Msg = MsgClient()
