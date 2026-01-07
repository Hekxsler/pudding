"""Utility functions for data types."""

import re

from .data import Data
from .or_ import Or
from .regex import Regex
from .string import String
from .varname import Varname

DATATYPES: list[type[Data]] = [String, Regex, Varname, Or]


def string_to_datatype(string: str, line: int) -> Data:
    """Convert a given string to a DataType.

    :param string: Value to convert.
    :param line: Line number of this value.
    :returns: The given value as a DataType.
    :raises TypeError: If there is no matching DataType.
    """
    for cls in DATATYPES:
        if re.fullmatch(cls.regex, string):
            return cls(line, string)
    msg = f"Unknown type of value {repr(string)} in line {line}"
    raise TypeError(f"{msg}, must be a string, regex or varname.")
