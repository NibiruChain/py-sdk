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
    chain_id: str
    fee_denom: str
    env: str
    websocket_endpoint: str = None

    def __post_init__(self):
        """
        Update the env value if the dataclass was created without one.
        """
        if self.env == "":
            self.env = "custom"

    @classmethod
    def devnet(cls) -> "Network":
        """
        Devnet is the network used for testing and debugging of the network. It is unstable and the version can change.

        Raises:
            KeyError: If the values are not set in the testing environment, this will raise an exception.

        Returns:
            Network: The updated Network object.
        """
        chain_config: Dict[str, Optional[str]] = {
            "HOST": os.getenv("HOST"),
            "GRPC_PORT": os.getenv("GRPC_PORT"),
            "LCD_PORT": os.getenv("LCD_PORT"),
            "CHAIN_ID": os.getenv("CHAIN_ID"),
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
            lcd_endpoint=f'http://{chain_config["HOST"]}:{chain_config["LCD_PORT"]}',
            grpc_endpoint=f'{chain_config["HOST"]}:{chain_config["GRPC_PORT"]}',
            websocket_endpoint=os.getenv("WEBSOCKET_ENDPOINT"),
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
    def local(cls) -> "Network":
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
