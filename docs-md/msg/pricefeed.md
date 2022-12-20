Module nibiru.msg.pricefeed
===========================

Classes
-------

`MsgPostPrice(oracle: str, token0: str, token1: str, price: float, expiry: datetime.datetime)`
:   Attributes:
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
