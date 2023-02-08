"""
The network class allows the user to defines the network the sdk interface should connect to.

There are some default values set for devnet, testnet, mainet and localnet, but the user cna also define its own
network by setting the values of the Network data class.

"""
import dataclasses
import enum
import os
from typing import Dict, List, Optional


@dataclasses.dataclass
class Network:
    """A representation of a Nibiru network based on its Tendermint RPC, gRPC,
    and LCD (REST) endpoints. A 'Network' instance enables interactions with a
    running blockchain.

    Attributes:
        lcd_endpoint (str): .
        grpc_endpoint (str): .
        tendermint_rpc_endpoint (str): .
        chain_id (str): .
        websocket_endpoint (str): .
        env (Optional[str]): TODO docs
        fee_denom (Optional[str]): Denom for the coin used to pay gas fees. Defaults to "unibi".

    Methods:
        customnet: A custom Nibiru network based on environment variables.
            Defaults to localnet.
        devnet: A development testnet environment that runs the latest release or
            pre-release from the nibiru repo. Defaults to 'nibiru-devnet-1'.
        localnet: The default local network created by running 'make localnet' in
            the nibiru repo.
        testnet: A stable testnet environment with public community members.
            Think of this as out practice mainnet. Defaults to 'nibiru-testnet-1'.
        mainnet: NotImplemented.

    Examples:
    >>> from nibiru import Network
    >>> network = Network.devnet(2)
    >>> network.is_insecure
    True
    """

    lcd_endpoint: str
    grpc_endpoint: str
    tendermint_rpc_endpoint: str
    chain_id: str
    websocket_endpoint: str
    env: str = "custom"
    fee_denom: str = "unibi"

    @property
    def is_insecure(self) -> bool:
        return not ("https" in self.tendermint_rpc_endpoint)

    @classmethod
    def customnet(cls) -> "Network":
        """
        Custom is the network configured from ENV variables.
        Defaults to localnet if no ENV variables are provided.

        Raises:
            KeyError: If the values are not set in the testing environment, this will raise an exception.

        Returns:
            Network: The updated Network object.
        """
        chain_config: Dict[str, Optional[str]] = {
            "LCD_ENDPOINT": os.getenv("LCD_ENDPOINT", "http://localhost:1317"),
            "GRPC_ENDPOINT": os.getenv("GRPC_ENDPOINT", "localhost:9090"),
            "TENDERMINT_RPC_ENDPOINT": os.getenv(
                "TENDERMINT_RPC_ENDPOINT", "http://localhost:26657"
            ),
            "WEBSOCKET_ENDPOINT": os.getenv(
                "WEBSOCKET_ENDPOINT", "ws://localhost:26657/websocket"
            ),
            "CHAIN_ID": os.getenv("CHAIN_ID", "nibiru-localnet-0"),
        }
        for name, env_var in chain_config.items():
            if env_var is None:
                raise KeyError(
                    "\n".join(
                        [
                            f"Environment variable {name} is needed for devnet.",
                            f"Please set {name} in your .env file.",
                        ]
                    )
                )

        return cls(
            lcd_endpoint=chain_config["LCD_ENDPOINT"],
            grpc_endpoint=chain_config["GRPC_ENDPOINT"],
            tendermint_rpc_endpoint=chain_config["TENDERMINT_RPC_ENDPOINT"],
            websocket_endpoint=chain_config["WEBSOCKET_ENDPOINT"],
            chain_id=chain_config["CHAIN_ID"],
            fee_denom='unibi',
            env="devnet",
        )

    @classmethod
    def testnet(cls, chain_num: int = 2) -> "Network":
        """
        Testnet is a network open to invited validators. It is more stable than
        devnet and provides a faucet to get some funds

        Args:
          chain_num (int): Testnet number

        Returns:
            Network: The updated Network object.
        """
        return cls(
            lcd_endpoint=f'https://lcd.testnet-{chain_num}.nibiru.fi',
            grpc_endpoint=f'tcp://grpc.testnet-{chain_num}.nibiru.fi:443',
            tendermint_rpc_endpoint=f'https://rpc.testnet-{chain_num}.nibiru.fi',
            websocket_endpoint=f'wss://rpc.testnet-{chain_num}.nibiru.fi/websocket',
            chain_id=f'nibiru-testnet-{chain_num}',
            fee_denom='unibi',
            env='testnet',
        )

    @classmethod
    def mainnet(cls) -> "Network":
        """
        Soon!
        """
        raise NotImplementedError

    @classmethod
    def localnet(cls) -> "Network":
        """
        Localnet is the network you would expect to connect to if you run `make localnet` from the nibiru repository.
        It allows you to update locally the golang codebase to checkout the behavior of the chain with different changes
        applied.

        Returns:
            Network: The updated Network object.
        """
        return cls(
            lcd_endpoint='http://localhost:1317',
            grpc_endpoint='localhost:9090',
            tendermint_rpc_endpoint='http://localhost:26657',
            websocket_endpoint='ws://localhost:26657/websocket',
            chain_id='nibiru-localnet-0',
            fee_denom='unibi',
            env='local',
        )

    def string(self) -> str:
        """
        Returns the current environment the network was initialized with. Will return `custom` if a custom network
        was created

        Returns:
            str: The name of the current environment.
        """
        return self.env

    @classmethod
    def devnet(cls, chain_num: int = 3) -> "Network":
        """
        Devnet is a network open to invited validators.

        Args:
          chain_num (int): Devnet number

        Returns:
            Network: The updated Network object.
        """
        return cls(
            lcd_endpoint=f'https://lcd.devnet-{chain_num}.nibiru.fi',
            grpc_endpoint=f'tcp://grpc.devnet-{chain_num}.nibiru.fi:443',
            tendermint_rpc_endpoint=f'https://rpc.devnet-{chain_num}.nibiru.fi:443',
            websocket_endpoint=f'wss://rpc.devnet-{chain_num}.nibiru.fi/websocket',
            chain_id=f'nibiru-devnet-{chain_num}',
            fee_denom='unibi',
            env='devnet',
        )

    @classmethod
    def from_chain_id(cls, chain_id: str) -> "Network":
        """
        Soon!
        """

        chain_id_elements: List[str] = chain_id.split("-")
        if len(chain_id_elements) != 3:
            raise ValueError(
                f"invalid chain_id format: {chain_id}. Expected one like nibiru-testnet-2"
            )

        prefix, chain_type, chain_number = chain_id_elements
        chain_number = int(chain_number)

        if chain_type == NetworkType.DEVNET.value:
            return Network.devnet(chain_number)
        elif chain_type == NetworkType.TESTNET.value:
            return Network.testnet(chain_number)
        elif chain_type == NetworkType.LOCALNET.value:
            return Network.localnet()
        else:
            network_types: List[str] = [member.value for member in NetworkType]
            raise ValueError(
                f"invalid chain type: {chain_type}. Available options: {network_types}"
            )


class NetworkType(enum.Enum):
    """Enum class for the available network types. E.g. 'testnet' and 'devnet'."""

    DEVNET = "devnet"
    TESTNET = "testnet"
    LOCALNET = "localnet"
