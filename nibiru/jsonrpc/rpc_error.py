class RPCError(Exception):
    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self) -> dict:
        error = {"code": self.code, "message": self.message}
        if self.data is not None:
            error["data"] = self.data
        return error

    @classmethod
    def from_dict(cls, d: dict) -> "RPCError":
        if not isinstance(d, dict):
            raise TypeError(f"Expected dict, got {type(d)}")

        # Check for required fields
        for dict_key in ["code", "message"]:
            if dict_key not in d:
                raise ValueError(f"Missing required field {dict_key}")

        # Create an RPCError object from the dictionary.
        code = d.get('code')
        message = d.get('message')
        data = d.get('data')
        return cls(code=code, message=message, data=data)


class ParseError(RPCError):
    def __init__(self, data=None):
        super().__init__(-32700, "Parse error", data)


class InvalidRequestError(RPCError):
    def __init__(self, data=None):
        super().__init__(-32600, "Invalid Request", data)


class MethodNotFoundError(RPCError):
    def __init__(self, data=None):
        super().__init__(-32601, "Method not found", data)


class InvalidParamsError(RPCError):
    def __init__(self, data=None):
        super().__init__(-32602, "Invalid params", data)


class InternalError(RPCError):
    def __init__(self, data=None):
        super().__init__(-32603, "Internal error", data)


class ServerError(RPCError):
    def __init__(self, code, data=None):
        if -32099 <= code <= -32000:
            super().__init__(code, "Server error", data)
        else:
            raise ValueError(
                "Code for ServerError should be within range (incusive) "
                + f"-32000 to -32099. Got code: {code}",
            )
