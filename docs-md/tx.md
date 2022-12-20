Module nibiru.tx
================

Classes
-------

`BaseTxClient(priv_key: nibiru.wallet.PrivateKey, network: nibiru.network.Network, client: nibiru.grpc_client.GrpcClient, config: nibiru.pytypes.common.TxConfig)`
:

    ### Methods

    `execute_msgs(self, msgs: Union[nibiru.pytypes.common.PythonMsg, List[nibiru.pytypes.common.PythonMsg]], get_sequence_from_node: bool = False, **kwargs) ‑> nibiru.pytypes.tx_resp.RawTxResp`
    :   Execute a message to broadcast a transaction to the node.
        Simulate the message to generate the gas estimate and send it to the node.
        If the transaction fail because of account sequence mismatch, we try to send it
        again once more with the sequence coming from a query to the lcd endpoint.

        Args:
            get_sequence_from_node (bool, optional): Specifies whether the sequence
                comes from the local value or the lcd endpoint. Defaults to False.

        Raises:
            TxError: Raw error log from the blockchain if the response code is nonzero.

        Returns:
            Union[RawTxResp, Dict[str, Any]]: The transaction response as a dict
                in proto3 JSON format.

    `execute_tx(self, tx: nibiru.transaction.Transaction, gas_estimate: float, **kwargs) ‑> cosmos.base.abci.v1beta1.abci_pb2.TxResponse`
    :

    `get_address_info(self)`
    :

    `get_config(self, **kwargs)`
    :   Properties in kwargs overwrite config

    `simulate(self, tx: nibiru.transaction.Transaction)`
    :
