"""Data type for a regular expression."""

from .data import Data


class Regex(Data):
    """Class representing a regular expression."""

    regex = r"\/(?:\\\/|[^\/])+\/"

    def __init__(self, line: int, value: str) -> None:
        """Init for Regex class."""
        super().__init__(line, value)
        self.value = value[1:-1]
        self.re_pattern = self.value
