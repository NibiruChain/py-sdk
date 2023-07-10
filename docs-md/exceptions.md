Module pysdk.exceptions
=======================

Classes
-------

`ErrorQueryTx(*args, **kwargs)`
:   Expresses failure to to query a tx with its hash.

    ### Ancestors (in MRO)

    * pysdk.exceptions.NibiruError
    * builtins.Exception
    * builtins.BaseException

`NibiruError(*args, **kwargs)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

    ### Descendants

    * pysdk.exceptions.ErrorQueryTx
    * pysdk.exceptions.QueryError
    * pysdk.exceptions.SimulationError
    * pysdk.exceptions.TxError

`QueryError(*args, **kwargs)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * pysdk.exceptions.NibiruError
    * builtins.Exception
    * builtins.BaseException

`SimulationError(*args, **kwargs)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * pysdk.exceptions.NibiruError
    * builtins.Exception
    * builtins.BaseException

`TxError(*args, **kwargs)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * pysdk.exceptions.NibiruError
    * builtins.Exception
    * builtins.BaseException
