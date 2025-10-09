"""Module defining datatype classes."""

import re
from re import Pattern


class Data:
    """Class representing a value."""

    regex: str
    value: str

    def __init__(self, value: str) -> None:
        """Init for Data class."""
        if not self.compile_re().fullmatch(value):
            raise TypeError(f"Value is not of datatype {self.__class__.__name__}")
        self.value = value

    def __str__(self) -> str:
        """Value as a string."""
        return self.value

    def __repr__(self) -> str:
        """String representation of a Data object."""
        return f"<{self.__class__.__name__} value={repr(self.value)}>"

    @classmethod
    def compile_re(cls) -> Pattern[str]:
        """Regex as a compiled Pattern object."""
        return re.compile(cls.regex)

    @property
    def pattern(self) -> Pattern[str]:
        """Value as a compiled Pattern object."""
        return re.compile(self.value)


class Or(Data):
    """Class representing an or-character."""

    regex = r"\|"


class String(Data):
    """Class representing a string value."""

    regex = r"\'(?:\\\'|[^\'])+\'"

    def __init__(self, value: str) -> None:
        """Init for String class."""
        super().__init__(value)
        self.value = value[1:-1]
    
    @property
    def pattern(self) -> Pattern[str]:
        """Value as a compiled Pattern object."""
        pattern = re.escape(self.value)
        return re.compile(pattern)


class Regex(Data):
    """Class representing a regular expression."""

    regex = r"\/(?:\\\/|[^\/])+\/"

    def __init__(self, value: str) -> None:
        """Init for Regex class."""
        super().__init__(value)
        self.value = value[1:-1]


class Varname(Data):
    """Class representing a variable name."""

    regex = r"\w+"


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
