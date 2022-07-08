import logging
from nibiru.sdks.tx.tx_client import TxClient
from .wallet import PrivateKey
from .client import Client
from .network import Network

class Sdk:
    def __init__(self, _error_do_not_use_init_directly=None) -> None:
        """Unsupported, please use from_mnemonic to initialize."""
        if not _error_do_not_use_init_directly:
            raise TypeError("Please use PrivateKey.from_mnemonic() to construct me")
        self._priv_key: PrivateKey = None
        self.query = None
        self.tx = None
        self._network = None

    @classmethod
    def authorize(cls, key: str = "") -> "Sdk":
        self = cls(_error_do_not_use_init_directly=True)
        if key == "":
            (mnemonic, pk) = PrivateKey.generate()
            logging.warning("The mnemonic used for the newly generated key is: %s", mnemonic)
            logging.warning("Please write down this key, it will NOT be recoverable otherwise")
        if len(key.split(" ")) > 1:
            pk = PrivateKey.from_mnemonic(key)
        elif len(key) > 0:
            pk = PrivateKey.from_hex(key)

        self.with_priv_key(pk)

        return self

    def with_network(self, network: Network) -> "Sdk":
        self._network = network
        self.with_query_client(Client(self._network, True))
        return self
        
    def with_query_client(self, client: Client) -> "Sdk":
        self.query = client
        self.tx = TxClient(client = client, network = self._network, priv_key = self._priv_key)
        return self

    def with_priv_key(self, priv_key: PrivateKey) -> "Sdk":
        self._priv_key = priv_key
        self._network = self.with_network(Network.local())
        return self

    @property
    def address(self):
        pub_key = self._priv_key.to_public_key()
        return pub_key.to_address().to_acc_bech32()