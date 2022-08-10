class Network:
    def __init__(
        self,
        lcd_endpoint: str,
        grpc_endpoint: str,
        chain_id: str,
        fee_denom: str,
        env: str,
    ):
        self.lcd_endpoint = lcd_endpoint
        self.grpc_endpoint = grpc_endpoint
        self.chain_id = chain_id
        self.fee_denom = fee_denom
        self.env = env

    @classmethod
    def devnet(cls) -> "Network":
        raise NotImplementedError

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
