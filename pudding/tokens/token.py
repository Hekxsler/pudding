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

    :var match_re: Regex matching the token in a string.
    :var value_re: Regex matching the user set values of this token.
    """

    match_re: Pattern[str]
    value_re: Pattern[str]

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
    def from_string(cls, string: str, lineno: int) -> Self:
        """Create Token object from string.

        :param string: String containing the token.
        :param lineno: Line number of the token.
        """
        raise NotImplementedError

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

    @classmethod
    def from_string(cls, string: str, lineno: int) -> Self:
        """Create Token object from string.

        :param string: String containing the token.
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


class MultiExpToken(BaseToken):
    """Token with an unknown amount of values."""

    value_types: tuple[*tuple[ValueType, ...], EllipsisType]

    @classmethod
    def from_string(cls, string: str, lineno: int) -> Self:
        """Parse a string into a MultiExpStatement object."""
        statement = cls.match_re.search(string)
        if not statement:
            raise ValueError("Statement not in given string.")
        name = statement.group(1)
        value_string = cls.value_re.search(statement.group(0))
        if value_string is None:
            raise ValueError("No values in statement.")
        values = re.findall(EXP_VAR, value_string.group(1))
        converted = (string_to_datatype(str(v), lineno) for v in values)
        return cls(lineno, name, tuple(converted))

    @classmethod
    def _get_value_types(cls) -> Generator[ValueType, None, None]:
        if len(cls.value_types) < 2:
            raise ValueError("MultiExpToken class needs at least two value types.")
        for t in cls.value_types:
            if isinstance(t, EllipsisType):
                break
            yield t
        yield cls.value_types[-2]
