"""Data type for a regular expression."""

import re
from typing import Pattern

from .data import Data


class Regex(Data):
    """Class representing a regular expression."""

    regex = r"\/(?:\\\/|[^\/])+\/"

    def __init__(self, value: str) -> None:
        """Init for Regex class."""
        super().__init__(value)
        self.value = value[1:-1]
        self._compiled: re.Pattern[str] | None = None

    @property
    def pattern(self) -> re.Pattern[str]:
        """Return compiled regex pattern, cached per instance."""
        if self._compiled is None:
            self._compiled = re.compile(self.value)
        return self._compiled
