Nibiru Constants
=================

Nibiru requires specific constants to be used to interact with the chain.

.. code:: python

    class TxType(Enum):
        SYNC = 1
        ASYNC = 2
        BLOCK = 3

    class Side(Enum):
        BUY = 1
        SELL = 2

    class Direction(Enum):
        ADD = 1
        REMOVE = 2


