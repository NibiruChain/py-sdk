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

    @classmethod
    def devnet(cls) -> "Network":
        chain_config: Dict[str, Optional[str]] = {
            "HOST": os.getenv("HOST"),
            "GRPC_PORT": os.getenv("GRPC_PORT"),
            "LCD_PORT": os.getenv("LCD_PORT"),
            "CHAIN_ID": os.getenv("CHAIN_ID"),
        }
        for name, env_var in chain_config.items():
            if env_var is None:
                raise Exception(
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
            chain_id=chain_config["CHAIN_ID"],
            fee_denom='unibi',
            env="devnet",
        )

    @classmethod
    def testnet(cls) -> "Network":
        return cls(
            lcd_endpoint='https://lcd.testnet-3.nibiru.fi',
            grpc_endpoint='grpc.testnet-3.nibiru.fi',
            chain_id='nibiru-testnet-3',
            fee_denom='unibi',
            env='testnet',
        )

    @classmethod
    def mainnet(cls) -> "Network":
        raise NotImplementedError

    @classmethod
    def local(cls) -> "Network":
        return cls(
            lcd_endpoint='http://localhost:1317',
            grpc_endpoint='localhost:9090',
            chain_id='nibiru-localnet-0',
            fee_denom='unibi',
            env='local',
        )

    def string(self):
        return self.env
