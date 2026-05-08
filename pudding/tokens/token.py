"""Module defining executable class."""

import re
from re import Pattern
from types import EllipsisType, UnionType
from typing import Any, Generator, NoReturn, Optional, Self, TypeVar

from ..datatypes import Data, String, string_to_datatype
from ..processor import PAction
from .util import EXP_VAR

_D = TypeVar("_D")
_T = TypeVar("_T", bound=tuple[Data, ...])
type ValueType = type[Data] | UnionType


class BaseToken:
    """Base class for tokens.

    :var match_re: Regex with two groups matching the token name and values
        in a line.
    :var value_delim_re: Regex matching the delimiter between values in the string
        matched by the match_re in group two.
    """

    match_re: Pattern[str]
    value_delim_re: Pattern[str]

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
        for value, value_type in zip(values, self._get_value_types()):
            if isinstance(value, value_type):
                continue
            is_type = value.__class__.__name__
            msg = f"Invalid argument of type {is_type} (expected {value_type})"
            raise TypeError(f"{msg} in line {self.lineno}")
        return values

    def __repr__(self) -> str:
        """Return string representation."""
        return f"<{self.lineno}, {self.name}, {self.values}>"

    @classmethod
    def _get_value_types(cls) -> Generator[ValueType, None, None]:
        raise NotImplementedError

    @classmethod
    def _match_values(cls, value_string: str) -> list[str]:
        match = re.match(EXP_VAR, value_string)
        values: list[str] = []
        while match is not None:
            values.append(match.group(0))
            value_string = value_string[len(match[0]):]
            if not value_string:
                return values
            delim = re.match(cls.value_delim_re, value_string)
            if not delim:
                raise SyntaxError("Invalid syntax of values in token.")
            value_string = value_string[len(delim[0]):]
            match = re.match(EXP_VAR, value_string)
            if not match:
                raise SyntaxError("Invalid syntax of values in token.")
        return values

    @classmethod
    def from_string(cls, string: str, lineno: int) -> Self:
        """Create Token object from string.

        :param string: String containing the token.
        :param lineno: Line number of the token.
        """
        token_match = cls.match_re.match(string)
        if token_match is None:
            raise ValueError("Token not in given string.")
        name = token_match.group(1)
        values = cls._match_values(token_match.group(2))
        return cls(lineno, name, tuple((string_to_datatype(v, lineno) for v in values)))

    @classmethod
    def matches(cls, string: str) -> bool:
        """Return bool if statement exists in the given string.

        :param string: String to search in.
        :returns: True if it exists.
        """
        return cls.match_re.match(string) is not None

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

    def get_string(self, index: int) -> String:
        """Get String object in values.

        :param index: Index of the object in values.
        :returns: The String object at the given index.
        :raises TypeError: If object at given index is not of type String.
        """
        value = self.values[index]
        if isinstance(value, String):
            return value
        raise TypeError(f"Value {repr(value)} is not a string. (line {self.lineno})")


class Token(BaseToken):
    """Token with a known number of values.

    :var value_types: Data types defining the type of the user set values.
    """

    value_types: tuple[ValueType, ...]

    @classmethod
    def _get_value_types(cls) -> Generator[ValueType, None, None]:
        return (t for t in cls.value_types)


class MultiExpToken(BaseToken):
    """Token with an unknown amount of values."""

    value_types: tuple[*tuple[ValueType, ...], EllipsisType]

    @classmethod
    def _get_value_types(cls) -> Generator[ValueType, None, None]:
        if len(cls.value_types) < 2:
            raise ValueError("MultiExpToken class needs at least two value types.")
        for t in cls.value_types:
            if isinstance(t, EllipsisType):
                break
            yield t
        yield cls.value_types[-2]
