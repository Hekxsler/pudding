"""Base class for data types."""

import re


class Data:
    """Class representing a data value.

    :var regex: Regex matching the data type as a string.
    :var value: Value of this data object.
    """

    regex: str
    value: str

    def __init__(self, value: str) -> None:
        """Init for Data class."""
        if not self.compile_re().fullmatch(value):
            raise TypeError(f"Value is not of type {self.__class__.__name__}")
        self.value = value

    def __str__(self) -> str:
        """Value as a string."""
        return self.value

    def __repr__(self) -> str:
        """String representation of a Data object."""
        return f"<{self.__class__.__name__} value={repr(self.value)}>"

    @classmethod
    def compile_re(cls) -> re.Pattern[str]:
        """Regex as a compiled Pattern object."""
        return re.compile(cls.regex)

    @property
    def pattern(self) -> re.Pattern[str]:
        """Value as a compiled Pattern object."""
        return re.compile(self.value)
