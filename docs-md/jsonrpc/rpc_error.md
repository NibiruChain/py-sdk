Module pysdk.jsonrpc.rpc_error
==============================

Classes
-------

`InternalError(data=None)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * pysdk.jsonrpc.rpc_error.RPCError
    * builtins.Exception
    * builtins.BaseException

`InvalidParamsError(data=None)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * pysdk.jsonrpc.rpc_error.RPCError
    * builtins.Exception
    * builtins.BaseException

`InvalidRequestError(data=None)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * pysdk.jsonrpc.rpc_error.RPCError
    * builtins.Exception
    * builtins.BaseException

`MethodNotFoundError(data=None)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * pysdk.jsonrpc.rpc_error.RPCError
    * builtins.Exception
    * builtins.BaseException

`ParseError(data=None)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * pysdk.jsonrpc.rpc_error.RPCError
    * builtins.Exception
    * builtins.BaseException

`RPCError(code, message, data=None)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

    ### Descendants

    * pysdk.jsonrpc.rpc_error.InternalError
    * pysdk.jsonrpc.rpc_error.InvalidParamsError
    * pysdk.jsonrpc.rpc_error.InvalidRequestError
    * pysdk.jsonrpc.rpc_error.MethodNotFoundError
    * pysdk.jsonrpc.rpc_error.ParseError
    * pysdk.jsonrpc.rpc_error.ServerError

    ### Static methods

    `from_dict(d: dict) ‑> pysdk.jsonrpc.rpc_error.RPCError`
    :

    ### Methods

    `to_dict(self) ‑> dict`
    :

`ServerError(code, data=None)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * pysdk.jsonrpc.rpc_error.RPCError
    * builtins.Exception
    * builtins.BaseException
