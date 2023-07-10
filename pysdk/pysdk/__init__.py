import sys

try:
    if sys.version_info >= (3, 8):
        from importlib.metadata import version

        __version__ = version(__package__ or __name__)
    else:
        import pkg_resources

        __version__ = pkg_resources.get_distribution(__package__ or __name__).version
except BaseException:
    pass

import google.protobuf.message

ProtobufMessage = google.protobuf.message.Message

import pysdk.exceptions  # noqa
import pysdk.pytypes  # noqa
from pysdk.grpc_client import GrpcClient  # noqa
from pysdk.msg import Msg  # noqa
from pysdk.pytypes import (  # noqa
    Coin,
    Direction,
    Network,
    NetworkType,
    PoolAsset,
    TxBroadcastMode,
    TxConfig,
)
from pysdk.sdk import Sdk  # noqa
from pysdk.tx import Transaction  # noqa
from pysdk.wallet import Address, PrivateKey, PublicKey  # noqa
