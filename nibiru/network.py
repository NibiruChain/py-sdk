"""
The network class allows the user to defines the network the sdk interface should connect to.

There are some default values set for devnet, testnet, mainet and localnet, but the user cna also define its own
network by setting the values of the Network data class.

"""
import dataclasses
import os
from typing import Dict, Optional


@dataclasses.dataclass
class Network:
    lcd_endpoint: str
    grpc_endpoint: str
    tendermint_rpc_endpoint: str
    chain_id: str
    env: str
    websocket_endpoint: str
    fee_denom: str = "unibi"

    def __post_init__(self):
        """
        Update the env value if the dataclass was created without one.
        """
        if self.env == "":
            self.env = "custom"

    @classmethod
    def customnet(cls) -> "Network":
        """
        Custom is the network configured from ENV variables. Defaults to localnet if no ENV variables are provided.

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
    def testnet(cls) -> "Network":
        """
        Testnet is a network open to invited validators. It is more stable than devnet and provides a faucet to get some
        funds

        Returns:
            Network: The updated Network object.
        """
        return cls(
            lcd_endpoint='https://lcd.testnet-3.nibiru.fi',
            grpc_endpoint='grpc.testnet-3.nibiru.fi',
            tendermint_rpc_endpoint='https://rpc.testnet-3.nibiru.fi',
            websocket_endpoint='wss://rpc.testnet-3.nibiru.fi/websocket',
            chain_id='nibiru-testnet-3',
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
