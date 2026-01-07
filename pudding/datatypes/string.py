"""Data type for a string."""

import re

from .data import Data


class String(Data):
    """Class representing a string value."""

    regex = r"\'(?:\\\'|[^\'])+\'"

    def __init__(self, line: int, value: str) -> None:
        """Init for String class."""
        super().__init__(line, value)
        self.value = value[1:-1]
        self.re_pattern = re.escape(self.value)
