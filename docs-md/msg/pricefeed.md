Module nibiru.msg.pricefeed
===========================

Classes
-------

`MsgPostPrice(oracle: str, token0: str, token1: str, price: float, expiry: datetime.datetime)`
:   PythonMsg corresponding to 'nibiru.pricefeed.v1.MsgPostPrice'.

    Attributes:
        oracle (str): address of the msg sender
        token0 (str): base asset denomination, e.g. ATOM
        token1 (str): quote asset denomination, e.g. USD
        price (float): price in units token1 / token0, e.g. price of ATOM in USD.
        expiry (datetime):

    ### Ancestors (in MRO)

    * nibiru.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `expiry: datetime.datetime`
    :

    `oracle: str`
    :

    `price: float`
    :

    `token0: str`
    :

    `token1: str`
    :

    ### Methods

    `to_pb(self) ‑> pricefeed.tx_pb2.MsgPostPrice`
    :   Returns the Message as protobuf object.

        Returns:
            pb.MsgPostPrice: The proto object.

`MsgsPricefeed()`
:   Messages for the x/pricefeed module.

    Methods:
    - post_price

    ### Methods

    `post_price(oracle: str, token0: str, token1: str, price: float, expiry: datetime.datetime) ‑> nibiru.msg.pricefeed.MsgPostPrice`
    :   Submits a price from 'oracle' on the specified token pair.

        Attributes:
            oracle (str): address of the msg sender
            token0 (str): base asset denomination, e.g. ATOM
            token1 (str): quote asset denomination, e.g. USD
            price (float): price in units token1 / token0, e.g. price of ATOM in USD.
            expiry (datetime):

        Returns:
            MsgPostPrice: PythonMsg corresponding to 'nibiru.pricefeed.v1.MsgPostPrice'.
