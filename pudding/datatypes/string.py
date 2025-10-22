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
        self._compiled_pattern: re.Pattern[str] | None = None

    @property
    def pattern(self) -> re.Pattern[str]:
        """Value as a compiled Pattern object."""
        # cache compiled pattern per instance to avoid repeatedly compiling
        if self._compiled_pattern is None:
            pattern = re.escape(self.value)
            self._compiled_pattern = re.compile(pattern)
        return self._compiled_pattern
