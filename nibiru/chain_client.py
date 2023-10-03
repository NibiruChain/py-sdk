from typing import Optional

from nibiru import Network, TxConfig
from nibiru.grpc_client import GrpcClient
from nibiru.tx import TxClient
from nibiru.wallet import PrivateKey


class ChainClient:
    """
    Main interface to the blockchain.

    Includes query client for sending gRPC queries
    and tx client for signing and broadcasting transactions if authorized.

    This object depends on the network and transaction configuration the users want.

    Examples:

    ```python
    from nibiru import ChainClient, Network, TxConfig, TxBroadcastMode

    # Default tx config
    client = ChainClient(Network.testnet(2))

    # Custom tx config
    client = ChainClient(
        Network.testnet(2),
        TxConfig(
            gas_price=0.5, gas_multiplier=1.5, broadcast_mode=TxBroadcastMode.SYNC,
        )
    )
    client.authorize(mnemonic="here goes the mnemonic ...")
    ```
    """

    _network: Network
    _query: GrpcClient
    _tx: Optional[TxClient]
    _private_key: Optional[PrivateKey]
    _address: Optional[str]

    def __init__(
        self,
        network: Network,
        tx_config: Optional[TxConfig] = None,
        check_version_compatibility: bool = True,
    ):
        """
        Create instance of the Nibiru chain client.
        Args:
            network: required. Chain network (devnet, testnet, mainnet).

            tx_config: optional. Set to customize default broadcast mode (sync, async)
                or gas settings.

            check_version_compatibility: set to false to skip version compatibility
                check between sdk and the chain. Default: true
        """
        if not network:
            raise ValueError("Parameter network is required")
        self._network = network

        self._query = GrpcClient(
            network,
            network.is_insecure,
            bypass_version_check=not check_version_compatibility,
        )
        self._tx = TxClient(
            client=self._query,
            network=network,
            config=tx_config or TxConfig(),
        )
        self._private_key = None
        self._address = None

    def authenticate(
        self,
        mnemonic: Optional[str] = None,
        private_key_hex: Optional[str] = None,
    ):
        """
        Authorize user by mnemonic or private key hex to sign transactions.
        """
        if mnemonic:
            private_key = PrivateKey.from_mnemonic(mnemonic)
        elif private_key_hex:
            private_key = PrivateKey.from_hex(private_key_hex)
        else:
            raise ValueError("Either mnemonic_key or private_key_hex must be provided")

        self._private_key = private_key
        self._tx.priv_key = private_key
        pub_key = self._private_key.to_public_key()
        self._address = pub_key.to_address().to_acc_bech32()

    def is_authenticated(self):
        """
        Returns true of user is authorized by mnemonic or private key, false otherwise
        """
        return self._private_key is not None

    @property
    def query(self):
        return self._query

    @property
    def tx(self):
        if not self.is_authenticated():
            raise ValueError("Not authenticated! Call authenticate() to use tx client")
        return self._tx

    @property
    def private_key(self):
        if not self.is_authenticated():
            raise ValueError(
                "Not authenticated! Call authenticate() to get private key"
            )
        return self._private_key

    @property
    def address(self):
        if not self.is_authenticated():
            raise ValueError(
                "Not authenticated! Call authenticate() to get your wallet address"
            )
        return self._address

    @property
    def network(self):
        return self._network
