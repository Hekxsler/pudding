"""Module defining executable class."""

from re import Pattern
from types import UnionType
from typing import Any, NoReturn, Optional, Self, TypeVar

from pudding.processor import PAction
from ..datatypes import Data, string_to_datatype


_D = TypeVar("_D")
_T = TypeVar("_T", bound=tuple[Data, ...])


class Token:
    """Base class for tokens.

    :var lineno: Line number of this token in the syntax file.
    :var match_re: Regex matching the token in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the user set values of this token.
    :vartype value_re: Pattern[str]
    :var value_types: Data types defining the type of the user set values.
    :vartype value_types: tuple[type | UnionType, ...]
    """

    match_re: Pattern[str]
    value_re: Pattern[str]
    value_types: tuple[type[Data] | UnionType, ...]

    def __init__(self, lineno: int, name: str, values: tuple[Data, ...]) -> None:
        """Init function for Token class.

        :param lineno: Line number.
        :param name: Name of this token.
        :param values: Tuple with string values of this token.
        """
        self.lineno = lineno
        self.name = name
        self.values = self._check_value_types(values)

    def _check_value_types(self, values: _T) -> _T:
        """Check if values are of the correct type.

        :param values: Tuple with values to check.
        :returns: The given tuple.
        :raises TypeError: If value is not the correct data type.
        """
        for value, value_type in zip(values, self.value_types):
            if isinstance(value, value_type):
                continue
            is_type = value.__class__.__name__
            expected = value_type.__class__.__name__
            msg = f"Invalid argument of type {is_type} (expected {expected})"
            raise TypeError(f"{msg} in line {self.lineno}")
        return values

    def __repr__(self) -> str:
        """Return string representation."""
        return f"<{self.lineno}, {self.name}, {self.values}>"

    @classmethod
    def from_string(cls, string: str, lineno: int) -> Self:
        """Create Function object from string.

        :param string: String containing the function.
        :param lineno: Line number of the token.
        """
        token_match = cls.match_re.search(string)
        if token_match is None:
            raise ValueError("Token not in given string.")
        name = token_match.group(1)
        value_match = cls.value_re.search(token_match.group(0))
        if value_match is None:
            raise ValueError("No values in token.")
        values = (str(x) for x in value_match.groups() if x is not None)
        return cls(lineno, name, tuple((string_to_datatype(v, lineno) for v in values)))

    @classmethod
    def matches(cls, string: str) -> bool:
        """Return bool if statement exists in the given string.

        :param string: String to search in.
        :returns: True if it exists.
        """
        return cls.match_re.search(string) is not None

    def execute(self, context: Any) -> PAction | NoReturn:
        """Execute this token.

        :param context: Context object.
        :returns: PAction for processor class.
        """
        raise NotImplementedError()

    def get_value(
        self, index: int, default: Optional[_D] = None
    ) -> Optional[_D] | Data:
        """Get a value.

        :param index: Index of the value in values tuple.
        :param default: Default value.
        :returns: The value at index or the default value if index is invalid.
        """
        if 0 < index < len(self.values):
            return self.values[index]
        return default
