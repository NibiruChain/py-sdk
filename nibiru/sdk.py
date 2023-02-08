"""
The "Sdk" is the main interface to the blockchain. Each "Sdk" object needs to be
authorized with a wallet/signer.

An "Sdk" includes a transaction client for signing and broadcasting transactions
and a query client for sending gRPC queries.

This object depends on the network and transaction configuration the users want.
These objects can be set using the Network and TxConfig classes from the
nibiru/pytypes package.
"""
import logging

from nibiru import pytypes
from nibiru.grpc_client import GrpcClient
from nibiru.tx import TxClient
from nibiru.wallet import PrivateKey


class Sdk:
    """The Sdk class creates an interface to sign and send transactions or execute
    queries from a node.

    It is associated to:
    - a wallet or signer, which can be newly generated or recovered from an
        existing mnemonic.
    - a network, defining the node to connect to
    - optionally a configuration defining how to behave and the gas configuration
        for each transaction

    Each method starting with `with_` will replace the existing Sdk object with a new version having the defined
    behavior.

    Attributes:
        priv_key
        query
        tx
        network
        tx_config


    Examples:

    ```python
    sdk = (
        Sdk.authorize(val_mnemonic)
        .with_config(tx_config)
        .with_network(network)
    )
    ```
    """

    query: GrpcClient
    network: pytypes.Network
    tx: TxClient
    tx_config: pytypes.TxConfig
    mnemonic: str

    def __init__(self, _error_do_not_use_init_directly=None) -> None:
        """Unsupported, please use from_mnemonic to initialize."""
        if not _error_do_not_use_init_directly:
            raise TypeError("Please use PrivateKey.from_mnemonic() to construct me")
        self.priv_key: PrivateKey = None
        self.query = None
        self.tx = None
        self.network = None
        self.tx_config = pytypes.TxConfig()

    @classmethod
    def authorize(cls, key: str = None) -> "Sdk":
        """
        Authorize allows the user to generate or recover a wallet and register it as an Sdk object.
        If a key is provided, the wallet will be recovered. Otherwise, a new wallet is created.

        Args:
            key (str, optional): The mnemonic if recover needed. Defaults to None.

        Returns:
            Sdk: The updated sdk object
        """
        self = cls(_error_do_not_use_init_directly=True)
        if key is None:
            (mnemonic, pk) = PrivateKey.generate()
            logging.warning(
                "The mnemonic used for the newly generated key is: \n%s", mnemonic
            )
            logging.warning(
                "Please write down this key, it will NOT be recoverable otherwise"
            )
        elif len(key.split(" ")) > 1:
            pk = PrivateKey.from_mnemonic(key)
        elif len(key) > 0:
            pk = PrivateKey.from_hex(key)

        self._with_priv_key(pk)
        self.mnemonic = mnemonic if key is None else key

        return self

    def with_network(
        self, network: pytypes.Network, bypass_version_check: bool = False
    ) -> "Sdk":
        """
        Change the network of the sdk to the specified network.

        Args:
            network (Network): A network object
            insecure (bool, optional): Wether the connection should be insecure or not. Defaults to False.
            bypass_version_check (bool, optional): Wether to bypass the check for correct version of the chain/py-sdk

        Returns:
            Sdk: The updated sdk object
        """
        self.network = network
        self._with_query_client(
            GrpcClient(network, network.is_insecure, bypass_version_check)
        )
        return self

    def with_config(self, config: pytypes.TxConfig) -> "Sdk":
        """
        Change the configuration for trasnactions for the sdk to the specified config.

        Args:
            config (TxConfig): A transaction configuration object

        Returns:
            Sdk: The updated sdk object
        """
        self.tx_config = config
        tx_client = TxClient(
            client=self.query,
            network=self.network,
            priv_key=self.priv_key,
            config=self.tx_config,
        )
        self._with_tx_client(tx_client)
        return self

    @property
    def address(self) -> str:
        """
        Returns the public address of the wallet.

        Returns:
            str: The public address of the wallet
        """
        pub_key = self.priv_key.to_public_key()
        return pub_key.to_address().to_acc_bech32()

    # Private methods
    def _with_query_client(self, client: GrpcClient) -> "Sdk":
        self.query = client
        tx_client = TxClient(
            client=self.query,
            network=self.network,
            priv_key=self.priv_key,
            config=self.tx_config,
        )
        self._with_tx_client(tx_client)
        return self

    def _with_tx_client(self, tx_client: TxClient) -> "Sdk":
        self.tx = tx_client
        return self

    def _with_priv_key(self, priv_key: PrivateKey) -> "Sdk":
        self.priv_key = priv_key
        return self
