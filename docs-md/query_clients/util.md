Module pysdk.query_clients.util
===============================

Variables
---------


`PROTOBUF_MSG_BASE_ATTRS: List[str]`
:   PROTOBUF_MSG_BASE_ATTRS (List[str]): The default attributes and methods of
    an instance of the 'protobuf.message.Message' class.

Functions
---------


`camel_to_snake(camel: str)`
:


`deserialize(pb_msg: google.protobuf.message.Message, no_sdk_transformation: bool = False) ‑> dict`
:   Deserializes a proto message into a dictionary.

    - sdk.Dec values are converted to floats.
    - sdk.Int values are converted to ints.
    - Missing fields become blank strings.

    Args:
        pb_msg (protobuf.message.Message)
        no_sdk_transformation (bool): Wether to bypass the sdk transformation. Default to False

    Returns:
        dict: 'pb_msg' as a JSON-able dictionary.


`deserialize_exp(proto_message: google.protobuf.message.Message) ‑> dict`
:   Take a proto message and convert it into a dictionnary.
    sdk.Dec values are converted to be consistent with txs.

    Args:
        proto_message (protobuf.message.Message)

    Returns:
        dict


`dict_keys_from_camel_to_snake(d)`
:   Transform all keys from the dictionary from camelcase to snake case.

    Args:
        d (dict): The dictionary to transform

    Returns:
        dict: The dictionary transformed


`get_block_messages(block: tendermint.types.block_pb2.Block) ‑> List[dict]`
:   Rerurns block messages as a list of dicts.
    Matches corresponding messages types by type_url.


`get_msg_pb_by_type_url(type_url: str) ‑> Optional[google.protobuf.message.Message]`
:   Tries loading protobuf class by type url.
    Examples type urls:
        /cosmos.bank.v1beta1.MsgSend
        /nibiru.perp.v1.MsgOpenPosition


`get_page_request(kwargs)`
:

Classes
-------

`QueryClient()`
:

    ### Descendants

    * pysdk.query_clients.auth.AuthQueryClient
    * pysdk.query_clients.epoch.EpochQueryClient
    * pysdk.query_clients.perp.PerpQueryClient
    * pysdk.query_clients.spot.SpotQueryClient
    * pysdk.query_clients.stablecoin.StablecoinQueryClient
    * pysdk.query_clients.staking.StakingQueryClient

    ### Methods

    `query(self, api_callable: grpc.UnaryUnaryMultiCallable, req: google.protobuf.message.Message, should_deserialize: bool = True, height: Optional[int] = None) ‑> Union[dict, google.protobuf.message.Message]`
    :
