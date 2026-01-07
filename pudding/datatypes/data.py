"""Base class for data types."""

import re


class Data:
    """Class representing a data value.

    :var regex: Regex matching the data type as a string.
    """

    regex: str

    def __init__(self, line: int, value: str) -> None:
        """Init for Data class.

        :param line: Line number of this data.
        :param value: Value of the data object.
        """
        if not re.fullmatch(self.regex, value):
            raise TypeError(f"Value is not of type {self.__class__.__name__}")
        self.line = line
        self.value = value
        self.re_pattern = re.escape(self.value)

    def __str__(self) -> str:
        """Value as a string."""
        return self.value

    def __repr__(self) -> str:
        """Return string representation of this object."""
        return f"<{self.__class__.__name__} value={repr(self.value)}>"
