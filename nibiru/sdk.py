import logging

from .client import Client
from .common import TxConfig
from .network import Network
from .sdks.tx import TxClient
from .wallet import PrivateKey


class Sdk:
    def __init__(self, _error_do_not_use_init_directly=None) -> None:
        """Unsupported, please use from_mnemonic to initialize."""
        if not _error_do_not_use_init_directly:
            raise TypeError("Please use PrivateKey.from_mnemonic() to construct me")
        self._priv_key: PrivateKey = None
        self.query = None
        self.tx = None
        self._network = None
        self.config = TxConfig()

    @classmethod
    def authorize(cls, key: str = "") -> "Sdk":
        self = cls(_error_do_not_use_init_directly=True)
        if key == "":
            (mnemonic, pk) = PrivateKey.generate()
            logging.warning("The mnemonic used for the newly generated key is: \n%s", mnemonic)
            logging.warning("Please write down this key, it will NOT be recoverable otherwise")
        if len(key.split(" ")) > 1:
            pk = PrivateKey.from_mnemonic(key)
        elif len(key) > 0:
            pk = PrivateKey.from_hex(key)

        self.with_priv_key(pk)

        return self

    def with_network(self, network: Network, insecure=False) -> "Sdk":
        self._network = network
        self.with_query_client(Client(self._network, insecure))
        return self

    def with_query_client(self, client: Client) -> "Sdk":
        self.query = client
        tx_client = TxClient(client=self.query, network=self._network, priv_key=self._priv_key, config=self.config)
        self.with_tx_client(tx_client)
        return self

    def with_tx_client(self, client: TxClient) -> "Sdk":
        self.tx = client
        return self

    def with_priv_key(self, priv_key: PrivateKey) -> "Sdk":
        self._priv_key = priv_key
        self.with_network(Network.local(), True)
        return self

    def with_config(self, config: TxConfig) -> "Sdk":
        self.config = config
        tx_client = TxClient(client=self.query, network=self._network, priv_key=self._priv_key, config=self.config)
        self.with_tx_client(tx_client)
        return self

    @property
    def address(self):
        pub_key = self._priv_key.to_public_key()
        return pub_key.to_address().to_acc_bech32()
