Module nibiru.network
=====================
The network class allows the user to defines the network the sdk interface should connect to.

There are some default values set for devnet, testnet, mainet and localnet, but the user cna also define its own
network by setting the values of the Network data class.

Classes
-------

`Network(lcd_endpoint: str, grpc_endpoint: str, tendermint_rpc_endpoint: str, chain_id: str, websocket_endpoint: str, env: str = 'custom', fee_denom: str = 'unibi')`
:   A representation of a Nibiru network based on its Tendermint RPC, gRPC,
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

    ### Class variables

    `chain_id: str`
    :

    `env: str`
    :

    `fee_denom: str`
    :

    `grpc_endpoint: str`
    :

    `lcd_endpoint: str`
    :

    `tendermint_rpc_endpoint: str`
    :

    `websocket_endpoint: str`
    :

    ### Static methods

    `customnet() ‑> nibiru.network.Network`
    :   Custom is the network configured from ENV variables.
        Defaults to localnet if no ENV variables are provided.

        Raises:
            KeyError: If the values are not set in the testing environment, this will raise an exception.

        Returns:
            Network: The updated Network object.

    `devnet(chain_num: int = 2) ‑> nibiru.network.Network`
    :   Devnet is a network open to invited validators.

        Args:
          chain_num (int): Devnet number

        Returns:
            Network: The updated Network object.

    `localnet() ‑> nibiru.network.Network`
    :   Localnet is the network you would expect to connect to if you run `make localnet` from the nibiru repository.
        It allows you to update locally the golang codebase to checkout the behavior of the chain with different changes
        applied.

        Returns:
            Network: The updated Network object.

    `mainnet() ‑> nibiru.network.Network`
    :   Soon!

    `testnet(chain_num: int = 1) ‑> nibiru.network.Network`
    :   Testnet is a network open to invited validators. It is more stable than
        devnet and provides a faucet to get some funds

        Args:
          chain_num (int): Testnet number

        Returns:
            Network: The updated Network object.

    ### Instance variables

    `is_insecure: bool`
    :

    ### Methods

    `string(self) ‑> str`
    :   Returns the current environment the network was initialized with. Will return `custom` if a custom network
        was created

        Returns:
            str: The name of the current environment.
