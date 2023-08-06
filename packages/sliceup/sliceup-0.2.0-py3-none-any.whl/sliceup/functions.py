# Unary functions
from typing import Union, Any


def id(name: str) -> dict:
    """Selects a column with id by given name.

    :param name: Column name
    :return: {Id: str}
    """
    return {'Id': name}


def alias(id: str, name: str) -> dict:
    """Creates 'name' alias of the selected column.

    :param id: Column id
    :param name: Column alias
    :return: {ColAlias: [{Id: str}, str]}
    """
    return {'ColAlias': [_to_id(id), name]}


def avg(id: str) -> dict:
    """Calculates the arithmetic mean of the selected column.

    :param id: Column id
    :return: {Avg: {Id: str}}
    """
    return {'Avg': _to_id(id)}


def bool_val(arg: bool) -> dict:
    """Creates the dictionary describing given boolean value.

    :param arg: Boolean value
    :return: {Bool: bool}
    """
    return {'Bool': arg}


def count(id: str) -> dict:
    """Counts the rows in the selected column.

    :param id: Column id
    :return: {Count: {Id: str}}
    """
    return {'Count': _to_id(id)}


def datetime(y: int, mm: int, dd: int, h: int = 0, m: int = 0, s: int = 0) -> dict:
    """Creates the dictionary describing datetime with given parameters.

    :param y: Year
    :param mm: Month
    :param dd: Day
    :param h: Hour
    :param m: Minute
    :param s: Second
    :return: {Datetime: str}
    """
    dt = f'{str(y)}/{str(mm).zfill(2)}/{str(dd).zfill(2)}' + \
         f'T{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}'

    return {'Datetime': dt}


def dev(id) -> dict:
    """Calculates the standard deviation of the selected column.

    :param id: Column id
    :return: {Dev: {Id: str}}
    """
    return {'Dev': _to_id(id)}


def float_val(arg: float) -> dict:
    """Creates the dictionary describing given float value.

    :param arg: Float value
    :return: {Float: float}
    """
    return {'Float': arg}


def int_val(arg: int) -> dict:
    """Creates the dictionary describing given integer value.

    :param arg: Integer value
    :return: {Int: int}
    """
    return {'Int': arg}


def last(id: str) -> dict:
    """Selects the last of the rows in the selected column.

    :param id: Column id
    :return: {Last: {Id: str}}
    """
    return {'Last': _to_id(id)}


def max(id: str) -> dict:
    """Finds the maximum value of the selected column.

    :param id: Column id
    :return: {Max: {Id: str}}
    """
    return {'Max': _to_id(id)}


def min(id: str) -> dict:
    """Finds the minimum value of the selected column.

    :param id: Column id
    :return: {Min: {Id: str}}
    """
    return {'Min': _to_id(id)}


def month(id) -> dict:
    """Gets the month of the selected column of type datetime.

    :param id: Column id
    :return: {Month: {Id: str}}
    """
    return {'Month': _to_id(id)}


def str_val(arg: str) -> dict:
    """Creates the dictionary describing given string value.

    :param arg: String value
    :return: {Str: str}
    """
    return {'Str': arg}


def sum(id: str) -> dict:
    """Calculates the sum of the selected column.

    :param id: Column id
    :return: {Sum: {Id: str}}
    """
    return {'Sum': _to_id(id)}


def sums(id: str) -> dict:
    """Calculates the rolling cumulative sum of the selected column.

    :param id: Column id
    :return: {Sums: {Id: str}}
    """
    return {'Sums': _to_id(id)}


def time(h: int, m: int, s: int) -> dict:
    """Creates the dictionary describing time with given parameters.

    :param h: Hour
    :param m: Minute
    :param s: Second
    :return: {Time: str}
    """
    t = f'{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}'

    return {'Time': t}


def unique(id: str) -> dict:
    """Finds all unique values in the selected column.

    :param id: Column id
    :return: {Unique: {Id: str}}
    """
    return {'Unique': _to_id(id)}


def variance(id: str) -> dict:
    """Calculates the variance of the selected columnn.

    :param id: Column id
    :return: {Var: {Id: str}}
    """
    return {'Var': _to_id(id)}


def year(id: str) -> dict:
    """Gets the year of the selected column of type datetime.

    :param id: Column id
    :return: {Year: {Id: str}}
    """
    return {'Year': _to_id(id)}


# Binary functions

def add(lhs: str, rhs: Union[int, float, dict]) -> dict:
    """Performs vectorized addition. Adds the value to the rows of the selected column.

    :param lhs: Column id
    :param rhs: Addition value
    :return: {Add: [{Id: str}, dict]}
    """
    return {'Add': [_to_id(lhs), _to_typed_expresion(rhs)]}


def bar(lhs: str, rhs: Any) -> dict:
    """Calculates bar values into buckets.

    :param lhs: Column id
    :param rhs: Distribution value
    :return: {Bar: [{Id: str}, dict]}
    """
    return {'Bar': [_to_id(lhs), _to_typed_expresion(rhs)]}


def div(lhs: str, rhs: Union[int, float, dict]) -> dict:
    """Performs vectorized division. Divides the selected column rows by the denominator value.

    :param lhs: Column id
    :param rhs: Denominator value
    :return: {Div: [{Id: str}, dict]}
    """
    return {'Div': [_to_id(lhs), _to_typed_expresion(rhs)]}


def ema(id: str, alpha: int) -> dict:
    """Calculates the exponential moving average of the selected column.

    :param id: Column id
    :param alpha: Distribution value
    :return: {Ema: [{Id: str}, dict]}
    """
    return {'Ema': [_to_id(id), int_val(alpha)]}


def eq(lhs: str, rhs: Any) -> dict:
    """Filters rows of the selected column equal to the given value.

    :param lhs: Column id
    :param rhs: Compared value
    :return: {Eq: [{Id: str}, dict]}
    """
    return {'Eq': [_to_id(lhs), _to_typed_expresion(rhs)]}


def gt(lhs: str, rhs: Union[int, float, dict]) -> dict:
    """Filters rows of the selected column greater than the given value.

    :param lhs: Column id
    :param rhs: Compared value
    :return: {Gt: [{Id: str}, dict]}
    """
    return {'Gt': [_to_id(lhs), _to_typed_expresion(rhs)]}


def gte(lhs: str, rhs: Union[int, float, dict]) -> dict:
    """Filters rows of the selected column greater than or equal to the given value.

    :param lhs: Column id
    :param rhs: Compared value
    :return: {Gte: [{Id: str}, dict]}
    """
    return {'Gte': [_to_id(lhs), _to_typed_expresion(rhs)]}


def lt(lhs: str, rhs: Union[int, float, dict]) -> dict:
    """Filters rows of the selected column lesser than the given value.

    :param lhs: Column id
    :param rhs: Compared value
    :return: {Lt: [{Id: str}, dict]}
    """
    return {'Lt': [_to_id(lhs), _to_typed_expresion(rhs)]}


def lte(lhs: str, rhs: Union[int, float, dict]) -> dict:
    """Filters rows of the selected column lesser than or equal to the given value.

    :param lhs: Column id
    :param rhs: Compared value
    :return: {Lte: [{Id: str}, dict]}
    """
    return {'Lte': [_to_id(lhs), _to_typed_expresion(rhs)]}


def mavg(id: str, lookback: int) -> dict:
    """Calculates the moving average of the selected column.

    :param id: Column id
    :param lookback: Number of points to look back from
    :return: {MAvg: [{Id: str}, dict]}
    """
    return {'MAvg': [_to_id(id), int_val(lookback)]}


def mdev(id: str, lookback: int) -> dict:
    """Calculates the moving standard deviation of the selected column.

    :param id: Column id
    :param lookback: Number of points to look back from
    :return: {MDev: [{Id: str}, dict]}
    """
    return {'MDev': [_to_id(id), int_val(lookback)]}


def mul(lhs: str, rhs: Union[int, float, dict]) -> dict:
    """Performs vectorized multiplication. Multiplies the selected column rows by the factor value.

    :param lhs: Column id
    :param rhs: Factor value
    :return: {Mul: [{Id: str}, dict]}
    """
    return {'Mul': [_to_id(lhs), _to_typed_expresion(rhs)]}


def neq(lhs: str, rhs: Any) -> dict:
    """Filters rows of the selected column not equal to the given value.

    :param lhs: Column id
    :param rhs: Compared value
    :return: {Neq: [{Id: str}, dict]}
    """
    return {'Neq': [_to_id(lhs), _to_typed_expresion(rhs)]}


def sub(lhs: str, rhs: Union[int, float, dict]) -> dict:
    """Performs vectorized subtraction. Subtracts the value from the rows of the selected column.

    :param lhs: Column id
    :param rhs: Subtraction value
    :return: {Sub: [{Id: str}, dict]}
    """
    return {'Sub': [_to_id(lhs), _to_typed_expresion(rhs)]}

# Helpers


def _to_id(arg):
    if isinstance(arg, str):
        arg = id(arg)
    return arg


def _to_typed_expresion(arg):
    if isinstance(arg, bool):
        return bool_val(arg)
    elif isinstance(arg, int):
        return int_val(arg)
    elif isinstance(arg, float):
        return float_val(arg)
    elif isinstance(arg, str):
        return str_val(arg)
    return arg
