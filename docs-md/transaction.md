Module nibiru.transaction
=========================

Classes
-------

`Transaction(msgs: Tuple[google.protobuf.message.Message, ...] = None, account_num: int = None, priv_key: nibiru.wallet.PrivateKey = None, sequence: int = None, chain_id: str = None, fee: List[cosmos.base.v1beta1.coin_pb2.Coin] = None, gas: int = 0, memo: str = '', timeout_height: int = 0)`
:

    ### Methods

    `get_sign_doc(self, public_key: nibiru.wallet.PublicKey = None) ‑> cosmos.tx.v1beta1.tx_pb2.SignDoc`
    :

    `get_signed_tx_data(self) ‑> bytes`
    :

    `get_tx_data(self, signature: bytes, public_key: nibiru.wallet.PublicKey = None) ‑> bytes`
    :

    `with_account_num(self, account_num: int) ‑> nibiru.transaction.Transaction`
    :

    `with_chain_id(self, chain_id: str) ‑> nibiru.transaction.Transaction`
    :

    `with_fee(self, fee: List[cosmos.base.v1beta1.coin_pb2.Coin]) ‑> nibiru.transaction.Transaction`
    :

    `with_gas(self, gas: numbers.Number) ‑> nibiru.transaction.Transaction`
    :

    `with_memo(self, memo: str) ‑> nibiru.transaction.Transaction`
    :

    `with_messages(self, msgs: Iterable[google.protobuf.message.Message]) ‑> nibiru.transaction.Transaction`
    :

    `with_sender(self, client: nibiru.grpc_client.GrpcClient, sender: str) ‑> nibiru.transaction.Transaction`
    :

    `with_sequence(self, sequence: int) ‑> nibiru.transaction.Transaction`
    :

    `with_signer(self, priv_key: nibiru.wallet.PrivateKey)`
    :

    `with_timeout_height(self, timeout_height: int) ‑> nibiru.transaction.Transaction`
    :
