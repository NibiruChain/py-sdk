from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp

from nibiru.exceptions import ConvertError, InvalidArgumentError

# number of decimal places
PRECISION = 18
INT_MULT = 1e6


# reimplementation of cosmos-sdk/types/decimal.go
def float_to_sdkdec(dec: float) -> str:
    '''
    create a decimal from an input decimal.
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
    '''
    dec_str = str(dec)

    if len(dec_str) == 0:
        raise InvalidArgumentError(f'Expected decimal string but got: {dec_str}')

    # first extract any negative symbol
    neg = False
    if dec_str[0] == '-':
        neg = True
        dec_str = dec_str[1:]

    if len(dec_str) == 0:
        raise InvalidArgumentError(f'Expected decimal string but got: {dec_str}')

    strs = dec_str.split('.')
    len_decs = 0
    combined_str = strs[0]

    if len(strs) == 2:  # has a decimal place
        len_decs = len(strs[1])
        if len_decs == 0 or len(combined_str) == 0:
            raise InvalidArgumentError(f'Expected decimal string but got: {dec_str}')
        combined_str += strs[1]
    elif len(strs) > 2:
        raise InvalidArgumentError(f'Expected decimal string but got: {dec_str}')

    if len_decs > PRECISION:
        raise InvalidArgumentError(
            f'value \'{dec_str}\' exceeds max precision by {PRECISION-len_decs} decimal places: max precision {PRECISION}'
        )

    # add some extra zero's to correct to the Precision factor
    zeros_to_add = PRECISION - len_decs
    zeros = '0' * zeros_to_add
    combined_str += zeros

    try:
        int(combined_str, 10)
    except ValueError as err:
        raise ConvertError(f'failed to set decimal string with base 10: {combined_str}') from err

    if neg:
        return '-' + combined_str

    return combined_str


def sdkdec_to_float(dec_str: str) -> float:
    if dec_str is None or dec_str == '':
        return 0

    if '.' in dec_str:
        raise InvalidArgumentError(f'expected a decimal string but got {dec_str} containing \'.\'')

    try:
        int(dec_str)
    except ValueError as err:
        raise ConvertError(f'failed to convert {dec_str} to a number') from err

    neg = False
    if dec_str[0] == '-':
        neg = True
        dec_str = dec_str[1:]

    input_size = len(dec_str)
    bz_str = ''
    # case 1, purely decimal
    if input_size <= PRECISION:
        # 0. prefix
        bz_str = '0.'

        # set relevant digits to 0
        bz_str += '0' * (PRECISION - input_size)

        # set final digits
        bz_str += dec_str
    else:
        # inputSize + 1 to account for the decimal point that is being added
        dec_point_place = input_size - PRECISION

        bz_str = dec_str[:dec_point_place]  # pre-decimal digits
        bz_str += '.'  # decimal point
        bz_str += dec_str[dec_point_place:]  # pre-decimal digits

    if neg:
        bz_str = '-' + bz_str

    return float(bz_str)


def float_to_sdkint(i: float) -> str:
    return str(int(i * INT_MULT))


def sdkint_to_float(int_str: str) -> float:
    return float(int_str) / INT_MULT


def toTsPb(dt: datetime):
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts
