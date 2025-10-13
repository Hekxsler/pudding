"""Data type for a variable name."""

from .data import Data


class Varname(Data):
    """Class representing a variable name."""

    regex = r"\w+"
