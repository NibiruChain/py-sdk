Module pysdk.msg.perp
=====================

Classes
-------

`Liquidation(pair: str, trader: str)`
:   Keeper of the pair/trader pairs for liquidations

    ### Class variables

    `pair: str`
    :

    `trader: str`
    :

`MsgAddMargin(sender: str, pair: str, margin: pysdk.pytypes.common.Coin)`
:   Add margin for the position (pair + trader)

    Attributes:
        sender (str): The trader address
        pair (str): The token pair
        margin (Coin): The margin to remove in a coin format

    ### Ancestors (in MRO)

    * pysdk.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `margin: pysdk.pytypes.common.Coin`
    :

    `pair: str`
    :

    `sender: str`
    :

    ### Methods

    `to_pb(self) ‑> nibiru.perp.v2.tx_pb2.MsgAddMargin`
    :   Returns the Message as protobuf object.

        Returns:
            pb.MsgAddMargin: The proto object.

`MsgClosePosition(sender: str, pair: str)`
:   Close the position.

    Attributes:
        sender (str): The sender address
        pair (str): The token pair

    ### Ancestors (in MRO)

    * pysdk.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `pair: str`
    :

    `sender: str`
    :

    ### Methods

    `to_pb(self) ‑> nibiru.perp.v2.tx_pb2.MsgClosePosition`
    :   Returns the Message as protobuf object.

        Returns:
            pb.MsgClosePosition: The proto object.

`MsgMarketOrder(sender: str, pair: str, dir: pysdk.pytypes.common.Direction, quote_asset_amount: float, leverage: float, base_asset_amount_limit: float)`
:   Open a position using the specified parameters.

    Attributes:
        sender (str): The sender address
        pair (str): The token pair
        side (Side): The side, either Side.BUY or Side.SELL
        quote_asset_amount (float): The quote amount you want to use to buy base
        leverage (float): The leverage you want to use, typically between 1 and 15, depending on the maintenance
            margin ratio of the pool.
        base_asset_amount_limit (float): The minimum amount of base you are willing to receive for this amount of
            quote.

    ### Ancestors (in MRO)

    * pysdk.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `base_asset_amount_limit: float`
    :

    `dir: pysdk.pytypes.common.Direction`
    :

    `leverage: float`
    :

    `pair: str`
    :

    `quote_asset_amount: float`
    :

    `sender: str`
    :

    ### Methods

    `to_pb(self) ‑> nibiru.perp.v2.tx_pb2.MsgMarketOrder`
    :   Returns the Message as protobuf object.

        Returns:
            pb.MsgMarketOrder: The proto object.

`MsgMultiLiquidate(sender: str, liquidations: List[pysdk.msg.perp.Liquidation])`
:   Close the position.

    Attributes:
        sender (str): The sender address
        liquidations (Liquidation): The list of {pair, trader} pairs.

    ### Ancestors (in MRO)

    * pysdk.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `liquidations: List[pysdk.msg.perp.Liquidation]`
    :

    `sender: str`
    :

    ### Methods

    `to_pb(self) ‑> nibiru.perp.v2.tx_pb2.MsgMultiLiquidate`
    :   Returns the Message as protobuf object.

        Returns:
            pb.MsgLiquidate: The proto object.

`MsgRemoveMargin(sender: str, pair: str, margin: pysdk.pytypes.common.Coin)`
:   Remove margin for the position (pair + trader)

    Attributes:
        sender (str): The trader address
        pair (str): The token pair
        margin (Coin): The margin to remove in a coin format

    ### Ancestors (in MRO)

    * pysdk.pytypes.common.PythonMsg
    * abc.ABC

    ### Class variables

    `margin: pysdk.pytypes.common.Coin`
    :

    `pair: str`
    :

    `sender: str`
    :

    ### Methods

    `to_pb(self) ‑> nibiru.perp.v2.tx_pb2.MsgRemoveMargin`
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

    ### Static methods

    `add_margin(sender: str, pair: str, margin: pysdk.pytypes.common.Coin) ‑> pysdk.msg.perp.MsgAddMargin`
    :   Add margin for the position (pair + trader)

        Attributes:
            sender (str): The trader address
            pair (str): The token pair
            margin (Coin): The margin to remove in a coin format

    `close_position(sender: str, pair: str) ‑> pysdk.msg.perp.MsgClosePosition`
    :   Close the position.

        Attributes:
            sender (str): The sender address
            pair (str): The token pair

    `liquidate(sender: str, pair: str, trader: str) ‑> pysdk.msg.perp.MsgMultiLiquidate`
    :   Liquidates unhealthy position (pair + trader)

        Attributes:
            sender (str): The liquidator address
            pair (str): The token pair
            trader (str): The trader address

    `liquidate_multiple(sender: str, liquidations: List[pysdk.msg.perp.Liquidation]) ‑> pysdk.msg.perp.MsgMultiLiquidate`
    :   Liquidates multiple unhealthy positions (pair + trader)

        Attributes:
            sender (str): The liquidator address
            liquidations (List[Liquidation]): list of pair/traders to liquidate

    `open_position(sender: str, pair: str, is_long: bool, quote_asset_amount: float, leverage: float, base_asset_amount_limit: float) ‑> pysdk.msg.perp.MsgMarketOrder`
    :   Open a posiiton using the specified parameters.

        Attributes:
            sender (str): The sender address
            pair (str): The token pair
            is_long (bool): Determines whether to open with long or short exposure.
            quote_asset_amount (float): The quote amount you want to use to buy base
            leverage (float): The leverage you want to use, typically between 1 and 15, depending on the maintenance
                margin ratio of the pool.
            base_asset_amount_limit (float): The minimum amount of base you are willing to receive for this amount of
                quote.

    `remove_margin(sender: str, pair: str, margin: pysdk.pytypes.common.Coin) ‑> pysdk.msg.perp.MsgRemoveMargin`
    :   Remove margin for the position (pair + trader)

        Attributes:
            sender (str): The trader address
            pair (str): The token pair
            margin (Coin): The margin to remove in a coin format

`perp()`
:   The perp class allows you to generate transaction for the perpetual futures module
    using the different messages available.

    ### Class variables

    `add_margin: pysdk.msg.perp.MsgAddMargin`
    :

    `close_position: pysdk.msg.perp.MsgClosePosition`
    :

    `liquidate: pysdk.msg.perp.MsgMultiLiquidate`
    :

    `open_position: pysdk.msg.perp.MsgMarketOrder`
    :

    `remove_margin: pysdk.msg.perp.MsgRemoveMargin`
    :
