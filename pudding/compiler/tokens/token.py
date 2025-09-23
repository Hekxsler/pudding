"""Module defining executable class."""

from re import Pattern
from types import UnionType
from typing import Any, NoReturn, Self, TypeVar

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
    value_types: tuple[type | UnionType, ...]

    def __init__(self, lineno: int, name: str, values: tuple[str, ...]) -> None:
        """Init function for Token class.

        :param lineno: Line number.
        :param name: Name of this token.
        :param values: Tuple with string values of this token.
        """
        self.lineno = lineno
        self.name = name
        converted: list[Data] = []
        for value in values:
            try:
                data = string_to_datatype(value)
            except TypeError as e:
                raise TypeError(
                    f"ERROR: Invalid data type {repr(value)} in line {lineno}"
                ) from e
            converted.append(data)
        self.values = self._check_value_types(tuple(converted))

    def _check_value_types(self, values: _T) -> _T:
        """Check if values are of the correct type.

        :param values: Tuple with values to check.
        :returns: The given tuple.
        :raises TypeError: If value is not the correct data type.
        """
        for value, _type in zip(values, self.value_types):
            if isinstance(value, _type):
                continue
            msg = f"Invalid argument of type {value.__class__.__name__}"
            raise TypeError(f"{msg} in line {self.lineno}")
        return values

    def __repr__(self) -> str:
        """String representation of a token."""
        return f"<{self.lineno}, {self.name}, {self.values}>"

    @classmethod
    def from_string(cls, string: str, lineno: int) -> Self:
        """Create Function object from string.

        :param string: String containing the function.
        :param lineno: Line number of the token.
        """
        raise NotImplementedError()

    @classmethod
    def matches(cls, string: str) -> bool:
        """Returns true if statement exists in the given string.

        :param string: String to search in.
        """
        return cls.match_re.search(string) is not None

    def execute(self, context: Any) -> PAction | NoReturn:
        """Execution function of this token.

        :param context: Context object.
        :type context: Context
        """
        raise NotImplementedError()

    def get_value(self, index: int, default: _D | None = None) -> _D | None | Data:
        """Get a value.

        :param index: Index of the value in values tuple.
        :param default: Default value.
        :returns: The value at index or the default value if index is invalid.
        """
        if 0 < index < len(self.values):
            return self.values[index]
        return default
