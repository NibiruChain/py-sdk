Module pysdk.utils
==================

Functions
---------


`clean_nested_dict(dictionary: Union[List[~T], Dict[~KT, ~VT], str]) ‑> Dict[~KT, ~VT]`
:   Takes a nested dictionnary with some values being string json values and convert it into a proper nested
    dictionary.

    Eg ::

        {
            "transaction_fee": "{"denom":"unusd","amount":"0"}",
            "funding_payment": "0.000000000000000000",
            "realized_pnl": "0.000000000000000000",
            "bad_debt": "{"denom":"unusd","amount":"0"}",
            "trader_address": "nibi1zaavvzxez0elundtn32qnk9lkm8kmcsz44g7xl",
            "margin": "{"denom":"unusd","amount":"10"}",
            "exchanged_position_size": "0.004999999999999500",
            "tx_hash": "12E496C996E39820B0807857CB7C19674BDD12DC8D789647D68C50BBB8C7D9CF"
        }

    becomes ::

        {
            "transaction_fee": {
                "denom": "unusd",
                "amount": "0"
            },
            "funding_payment": "0.000000000000000000",
            "realized_pnl": "0.000000000000000000",
            "bad_debt": {
                "denom": "unusd",
                "amount": "0"
            },
            "trader_address": "nibi1zaavvzxez0elundtn32qnk9lkm8kmcsz44g7xl",
            "margin": {
                "denom": "unusd",
                "amount": "10"
            },
            "exchanged_position_size": "0.004999999999999500",
            "tx_hash": "12E496C996E39820B0807857CB7C19674BDD12DC8D789647D68C50BBB8C7D9CF"
        }

    Args:
        dictionary (Union[List, Dict, str]): The dictionary to be converted.

    Returns:
        Dict: A converted dictionary.


`dict_keys_must_match(dict_: dict, keys: List[str])`
:   Asserts that two iterables have the same elements, the same number of
    times, without regard to order.
    Alias for the 'element_counts_are_equal' function.

    dict_keys_must_match(dict_, keys)

    Example:
    - [0, 1, 1] and [1, 0, 1] compare equal.
    - [0, 0, 1] and [0, 1] compare unequal.


`element_counts_are_equal(first: Iterable[Any], second: Iterable[Any]) ‑> Optional[bool]`
:   Asserts that two iterables have the same elements, the same number of
    times, without regard to order.

    Args:
        first (Iterable[Any])
        second (Iterable[Any])

    Returns:
        Optional[bool]: "passed" status. If this is True, first and second share
            the same element counts. If they don't the function will raise an
            AssertionError and return 'None'.


`format_fields_nested(object: Union[list, dict], fn: Callable[[Any], Any], fields: List[str]) ‑> Union[list, dict]`
:   Format the fields inside a nested dictionary with the function provided

    Args:
        object (Union[list, dict]): The object to format
        fn (Callable[[Any], Any]): The function to format objects with
        fields (list[str]): The fields to format

    Returns:
        Union[list, dict]: The output formatted


`from_sdk_dec(dec_str: str) ‑> float`
:


`from_sdk_dec_n(dec_str: str, n: int = 6) ‑> float`
:


`from_sdk_int(int_str: str) ‑> int`
:


`toPbTimestamp(dt: datetime.datetime)`
:


`to_sdk_dec(dec: float) ‑> str`
:   create a decimal from an input decimal.
    valid must come in the form:
        (-) whole integers (.) decimal integers
    examples of acceptable input include:
        -123.456
        456.7890
        345
        -456789

    NOTE - An error will return if more decimal places
    are provided in the string than the constant Precision.

    CONTRACT - This function does not mutate the input str.


`to_sdk_int(i: float) ‑> str`
:

Classes
-------

`ColoredFormatter(fmt=None, datefmt=None, style='%', validate=True)`
:   Formatter instances are used to convert a LogRecord to text.

    Formatters need to know how a LogRecord is constructed. They are
    responsible for converting a LogRecord to (usually) a string which can
    be interpreted by either a human or an external system. The base Formatter
    allows a formatting string to be specified. If none is supplied, the
    style-dependent default value, "%(message)s", "{message}", or
    "${message}", is used.

    The Formatter can be initialized with a format string which makes use of
    knowledge of the LogRecord attributes - e.g. the default value mentioned
    above makes use of the fact that the user's message and arguments are pre-
    formatted into a LogRecord's message attribute. Currently, the useful
    attributes in a LogRecord are described by:

    %(name)s            Name of the logger (logging channel)
    %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                        WARNING, ERROR, CRITICAL)
    %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                        "WARNING", "ERROR", "CRITICAL")
    %(pathname)s        Full pathname of the source file where the logging
                        call was issued (if available)
    %(filename)s        Filename portion of pathname
    %(module)s          Module (name portion of filename)
    %(lineno)d          Source line number where the logging call was issued
                        (if available)
    %(funcName)s        Function name
    %(created)f         Time when the LogRecord was created (time.time()
                        return value)
    %(asctime)s         Textual time when the LogRecord was created
    %(msecs)d           Millisecond portion of the creation time
    %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                        relative to the time the logging module was loaded
                        (typically at application startup time)
    %(thread)d          Thread ID (if available)
    %(threadName)s      Thread name (if available)
    %(process)d         Process ID (if available)
    %(message)s         The result of record.getMessage(), computed just as
                        the record is emitted

    Initialize the formatter with specified format strings.

    Initialize the formatter either with the specified format string, or a
    default as described above. Allow for specialized date formatting with
    the optional datefmt argument. If datefmt is omitted, you get an
    ISO8601-like (or RFC 3339-like) format.

    Use a style parameter of '%', '{' or '$' to specify that you want to
    use one of %-formatting, :meth:`str.format` (``{}``) formatting or
    :class:`string.Template` formatting in your format string.

    .. versionchanged:: 3.2
       Added the ``style`` parameter.

    ### Ancestors (in MRO)

    * logging.Formatter

    ### Class variables

    `FORMATS`
    :

    `bold_red`
    :

    `cyan`
    :

    `fmt`
    :

    `green`
    :

    `grey`
    :

    `red`
    :

    `reset`
    :

    `white`
    :

    `yellow`
    :

    ### Methods

    `format(self, record: logging.LogRecord)`
    :   Formats a record for the logging handler.

        Args:
            record (logging.LogRecord): Represents an instance of an event being
                logged.
