"""Data type for a string."""

import re

from .data import Data


class String(Data):
    """Class representing a string value."""

    regex = r"\'(?:\\\'|[^\'])+\'"

    def __init__(self, value: str) -> None:
        """Init for String class."""
        super().__init__(value)
        self.value = value[1:-1]

    @property
    def pattern(self) -> re.Pattern[str]:
        """Value as a compiled Pattern object."""
        pattern = re.escape(self.value)
        return re.compile(pattern)
