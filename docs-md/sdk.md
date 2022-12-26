Module nibiru.sdk
=================
The "Sdk" is the main interface to the blockchain. Each "Sdk" object needs to be
authorized with a wallet/signer.

An "Sdk" includes a transaction client for signing and broadcasting transactions
and a query client for sending gRPC queries.

This object depends on the network and transaction configuration the users want.
These objects can be set using the Network and TxConfig classes from the
nibiru/pytypes package.

Classes
-------

`Sdk()`
:   The Sdk class creates an interface to sign and send transactions or execute
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
        .with_network(network, network_insecure)
    )
    ```

    Unsupported, please use from_mnemonic to initialize.

    ### Class variables

    `network: nibiru.pytypes.network.Network`
    :

    `query: nibiru.grpc_client.GrpcClient`
    :

    `tx: nibiru.tx.TxClient`
    :

    `tx_config: nibiru.pytypes.common.TxConfig`
    :

    ### Static methods

    `authorize(key: str = None) ‑> nibiru.sdk.Sdk`
    :   Authorize allows the user to generate or recover a wallet and register it as an Sdk object.
        If a key is provided, the wallet will be recovered. Otherwise, a new wallet is created.

        Args:
            key (str, optional): The mnemonic if recover needed. Defaults to None.

        Returns:
            Sdk: The updated sdk object

    ### Instance variables

    `address: str`
    :   Returns the public address of the wallet.

        Returns:
            str: The public address of the wallet

    ### Methods

    `with_config(self, config: nibiru.pytypes.common.TxConfig) ‑> nibiru.sdk.Sdk`
    :   Change the configuration for trasnactions for the sdk to the specified config.

        Args:
            config (TxConfig): A transaction configuration object

        Returns:
            Sdk: The updated sdk object

    `with_network(self, network: nibiru.pytypes.network.Network, bypass_version_check: bool = False) ‑> nibiru.sdk.Sdk`
    :   Change the network of the sdk to the specified network.

        Args:
            network (Network): A network object
            insecure (bool, optional): Wether the connection should be insecure or not. Defaults to False.
            bypass_version_check (bool, optional): Wether to bypass the check for correct version of the chain/py-sdk

        Returns:
            Sdk: The updated sdk object
