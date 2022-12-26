Module nibiru.msg.perp
======================

Classes
-------

`MsgAddMargin(sender: str, token_pair: str, margin: nibiru.pytypes.common.Coin)`
:   Add margin for the position (token_pair + trader)

    Attributes:
        sender (str): The trader address
        token_pair (str): The token pair
        margin (Coin): The margin to remove in a coin format

    ### Ancestors (in MRO)

    * nibiru.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `margin: nibiru.pytypes.common.Coin`
    :

    `sender: str`
    :

    `token_pair: str`
    :

    ### Methods

    `to_pb(self) ‑> perp.v1.tx_pb2.MsgAddMargin`
    :   Returns the Message as protobuf object.

        Returns:
            pb.MsgAddMargin: The proto object.

`MsgClosePosition(sender: str, token_pair: str)`
:   Close the position.

    Attributes:
        sender (str): The sender address
        token_pair (str): The token pair

    ### Ancestors (in MRO)

    * nibiru.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `sender: str`
    :

    `token_pair: str`
    :

    ### Methods

    `to_pb(self) ‑> perp.v1.tx_pb2.MsgClosePosition`
    :   Returns the Message as protobuf object.

        Returns:
            pb.MsgClosePosition: The proto object.

`MsgLiquidate(sender: str, token_pair: str, trader: str)`
:   Close the position.

    Attributes:
        sender (str): The sender address
        token_pair (str): The token pair

    ### Ancestors (in MRO)

    * nibiru.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `sender: str`
    :

    `token_pair: str`
    :

    `trader: str`
    :

    ### Methods

    `to_pb(self) ‑> perp.v1.tx_pb2.MsgLiquidate`
    :   Returns the Message as protobuf object.

        Returns:
            pb.MsgLiquidate: The proto object.

`MsgOpenPosition(sender: str, token_pair: str, side: nibiru.pytypes.common.Side, quote_asset_amount: float, leverage: float, base_asset_amount_limit: float)`
:   Open a position using the specified parameters.

    Attributes:
        sender (str): The sender address
        token_pair (str): The token pair
        side (Side): The side, either Side.BUY or Side.SELL
        quote_asset_amount (float): The quote amount you want to use to buy base
        leverage (float): The leverage you want to use, typically between 1 and 15, depending on the maintenance
            margin ratio of the pool.
        base_asset_amount_limit (float): The minimum amount of base you are willing to receive for this amount of
            quote.

    ### Ancestors (in MRO)

    * nibiru.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `base_asset_amount_limit: float`
    :

    `leverage: float`
    :

    `quote_asset_amount: float`
    :

    `sender: str`
    :

    `side: nibiru.pytypes.common.Side`
    :

    `token_pair: str`
    :

    ### Methods

    `to_pb(self) ‑> perp.v1.tx_pb2.MsgOpenPosition`
    :   Returns the Message as protobuf object.

        Returns:
            pb.MsgOpenPosition: The proto object.

`MsgRemoveMargin(sender: str, token_pair: str, margin: nibiru.pytypes.common.Coin)`
:   Remove margin for the position (token_pair + trader)

    Attributes:
        sender (str): The trader address
        token_pair (str): The token pair
        margin (Coin): The margin to remove in a coin format

    ### Ancestors (in MRO)

    * nibiru.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `margin: nibiru.pytypes.common.Coin`
    :

    `sender: str`
    :

    `token_pair: str`
    :

    ### Methods

    `to_pb(self) ‑> perp.v1.tx_pb2.MsgRemoveMargin`
    :   Returns the Message as protobuf object.

        Returns:
            pb.MsgRemoveMargin: The proto object.

`MsgsPerp()`
:   Messages for the Nibiru Chain x/perp module

    Methods:
    - open_position
    - close_position:
    - add_margin: Deleverages a position by adding margin to back it.
    - remove_margin: Increases the leverage of the position by removing margin.

    ### Methods

    `add_margin(sender: str, token_pair: str, margin: nibiru.pytypes.common.Coin) ‑> nibiru.msg.perp.MsgAddMargin`
    :   Add margin for the position (token_pair + trader)

        Attributes:
            sender (str): The trader address
            token_pair (str): The token pair
            margin (Coin): The margin to remove in a coin format

    `close_position(sender: str, token_pair: str) ‑> nibiru.msg.perp.MsgClosePosition`
    :   Close the position.

        Attributes:
            sender (str): The sender address
            token_pair (str): The token pair

    `open_position(sender: str, token_pair: str, is_long: bool, quote_asset_amount: float, leverage: float, base_asset_amount_limit: float) ‑> nibiru.msg.perp.MsgOpenPosition`
    :   Open a posiiton using the specified parameters.

        Attributes:
            sender (str): The sender address
            token_pair (str): The token pair
            is_long (bool): Determines whether to open with long or short exposure.
            quote_asset_amount (float): The quote amount you want to use to buy base
            leverage (float): The leverage you want to use, typically between 1 and 15, depending on the maintenance
                margin ratio of the pool.
            base_asset_amount_limit (float): The minimum amount of base you are willing to receive for this amount of
                quote.

    `remove_margin(sender: str, token_pair: str, margin: nibiru.pytypes.common.Coin) ‑> nibiru.msg.perp.MsgRemoveMargin`
    :   Remove margin for the position (token_pair + trader)

        Attributes:
            sender (str): The trader address
            token_pair (str): The token pair
            margin (Coin): The margin to remove in a coin format

`perp()`
:   The perp class allows you to generate transaction for the perpetual futures module using the different messages
    available.

    ### Class variables

    `add_margin: nibiru.msg.perp.MsgAddMargin`
    :

    `close_position: nibiru.msg.perp.MsgClosePosition`
    :

    `liquidate: nibiru.msg.perp.MsgLiquidate`
    :

    `open_position: nibiru.msg.perp.MsgOpenPosition`
    :

    `remove_margin: nibiru.msg.perp.MsgRemoveMargin`
    :
