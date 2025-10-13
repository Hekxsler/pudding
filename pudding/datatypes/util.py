"""Utility functions for data types."""

from .data import Data
from .or_ import Or
from .regex import Regex
from .string import String
from .varname import Varname

DATATYPES: list[type[Data]] = [String, Regex, Varname, Or]


def string_to_datatype(string: str) -> Data:
    """Convert a given string to a DataType.

    :param string: Value to convert.
    :returns: The given value as a DataType.
    :raises TypeError: If there is no matching DataType.
    """
    for cls in DATATYPES:
        if cls.compile_re().fullmatch(string):
            return cls(string)
    raise TypeError(
        f"Unknown type of value {repr(string)}, must be a string, regex or varname."
    )
