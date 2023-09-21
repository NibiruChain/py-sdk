Module pysdk.wallet
===================

Classes
-------

`Address(addr: bytes)`
:

    ### Class variables

    `addr: bytes`
    :

    `number: int`
    :

    `sequence: int`
    :

    ### Static methods

    `from_acc_bech32(bech: str) ‑> pysdk.wallet.Address`
    :   Create an address instance from a bech32-encoded account address

    `from_cons_bech32(bech: str) ‑> pysdk.wallet.Address`
    :   Create an address instance from a bech32-encoded consensus address

    `from_val_bech32(bech: str) ‑> pysdk.wallet.Address`
    :   Create an address instance from a bech32-encoded validator address

    ### Methods

    `decrease_sequence(self)`
    :   If a tx failed the sequence should not increase

    `get_number(self)`
    :

    `get_sequence(self, from_node=False, lcd_endpoint: str = None) ‑> int`
    :   Get the sequence number from the module. If from node is set to true, update our local indice with a query to
        the node.

        Args:
            from_node (bool, optional): Whether to query or not from the node. Defaults to False.
            lcd_endpoint (str, optional): The lcd endoint, needed for when from_node is set to true. Defaults to None.

        Returns:
            int: the current sequence number

    `get_subaccount_id(self, index: int) ‑> str`
    :   Return a hex representation of address

    `init_num_seq(self, lcd_endpoint: str) ‑> pysdk.wallet.Address`
    :

    `to_acc_bech32(self) ‑> str`
    :   Return a bech32-encoded account address

    `to_cons_bech32(self) ‑> str`
    :   Return a bech32-encoded with consensus address

    `to_hex(self) ‑> str`
    :   Return a hex representation of address

    `to_val_bech32(self) ‑> str`
    :   Return a bech32-encoded validator address

`PrivateKey()`
:   Class for wrapping SigningKey that is used for signature creation and public key derivation.

    :ivar signing_key: the ecdsa SigningKey instance
    :vartype signing_key: ecdsa.SigningKey

    Unsupported, please use from_mnemonic to initialize.

    ### Static methods

    `from_hex(priv: str) ‑> pysdk.wallet.PrivateKey`
    :

    `from_mnemonic(words: str, path="m/44'/118'/0'/0/0") ‑> pysdk.wallet.PrivateKey`
    :   Create a PrivateKey instance from a given mnemonic phrase and a HD derivation path.
        If path is not given, default to Band's HD prefix 494 and all other indexes being zeroes.

        :param words: the mnemonic phrase for recover private key
        :param path: the HD path that follows the BIP32 standard

        :return: Initialized PrivateKey object

    `generate(path="m/44'/118'/0'/0/0") ‑> Tuple[str, pysdk.wallet.PrivateKey]`
    :   Generate new private key with random mnemonic phrase

        :param path: the HD path that follows the BIP32 standard

        Returns:
            Tuple[Mnemonic, 'PrivateKey']: A tuple of mnemonic phrase and PrivateKey instance

    ### Methods

    `sign(self, msg: bytes) ‑> bytes`
    :   Sign the given message using the edcsa sign_deterministic function.

        :param msg: the message that will be hashed and signed

        :return: a signature of this private key over the given message

    `to_hex(self) ‑> str`
    :   Return a hex representation of signing key.

    `to_public_key(self) ‑> pysdk.wallet.PublicKey`
    :   Return the PublicKey associated with this private key.

        :return: a PublicKey that can be used to verify the signatures made with this PrivateKey

`PubKeyProto(*args, **kwargs)`
:   A ProtocolMessage

    ### Ancestors (in MRO)

    * google._upb._message.Message
    * google.protobuf.message.Message

    ### Class variables

    `DESCRIPTOR`
    :

`PublicKey()`
:   Class for wrapping VerifyKey using for signature verification. Adding method to encode/decode
    to Bech32 format.

    :ivar verify_key: the ecdsa VerifyingKey instance
    :vartype verify_key: ecdsa.VerifyingKey

    Unsupported, please do not construct it directly.

    ### Static methods

    `from_acc_bech32(bech: str) ‑> pysdk.wallet.PublicKey`
    :

    `from_cons_bech32(bech: str) ‑> pysdk.wallet.PublicKey`
    :

    `from_val_bech32(bech: str) ‑> pysdk.wallet.PublicKey`
    :

    ### Methods

    `to_acc_bech32(self) ‑> str`
    :   Return bech32-encoded with account public key prefix

    `to_address(self) ‑> pysdk.wallet.Address`
    :   Return address instance from this public key

    `to_cons_bech32(self) ‑> str`
    :   Return bech32-encoded with validator consensus public key prefix

    `to_hex(self) ‑> str`
    :   Return a hex representation of verified key.

    `to_public_key_proto(self) ‑> cosmos.crypto.secp256k1.keys_pb2.PubKey`
    :

    `to_val_bech32(self) ‑> str`
    :   Return bech32-encoded with validator public key prefix

    `verify(self, msg: bytes, sig: bytes) ‑> bool`
    :   Verify a signature made from the given message.

        :param msg: data signed by the `signature`, will be hashed using sha256 function
        :param sig: encoding of the signature

        :raises BadSignatureError: if the signature is invalid or malformed
        :return: True if the verification was successful
