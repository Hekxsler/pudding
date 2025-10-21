"""Module defining statements."""

import re
from typing import Self, TypeVar

from ...datatypes import Data, Or, Varname, string_to_datatype
from ...processor import PAction
from ...processor.context import Context
from ..token import Token
from ..util import EXP_VAR

_T = TypeVar("_T", bound=tuple[Data, ...])


class Statement(Token):
    """Base class for a statement."""

    def execute(self, context: Context) -> PAction:
        """Execute this token.

        :param context: Current context object.
        :returns: PAction for processor class.
        """
        raise NotImplementedError()


class MultiExpStatement(Statement):
    """Base class for a statement with multiple expressions."""

    value_types = (Data,)

    def _check_value_types(self, values: _T) -> _T:
        """Check type of all values."""
        for value in values:
            if isinstance(value, self.value_types[0]):
                continue
            raise TypeError(
                f"Invalid argument for {self.name} statement in line {self.lineno}"
            )
        return values

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
        values = re.findall(rf"{EXP_VAR}", value_string.group(1))
        converted: list[Data] = []
        for value in values:
            try:
                data = string_to_datatype(value)
            except TypeError as e:
                raise TypeError(
                    f"ERROR: Invalid data type {repr(value)} in line {lineno}"
                ) from e
            converted.append(data)
        return cls(lineno, name, tuple(converted))

    def get_patterns(self, context: Context) -> list[str]:
        """Return the combined patterns as a string.

        :param context: Context to resolve variables.
        :returns: List of regex patterns, where each element is a possible pattern.
        """
        patterns = [r""]
        for data in self.values:
            if isinstance(data, Or):
                patterns.append(r"")
                continue
            if isinstance(data, Varname):
                value = context.get_var(data.value)
            else:
                value = data.pattern
            patterns[-1] += rf"({value.pattern})"
        return patterns

    def execute(self, context: Context) -> PAction:
        """Execute this token.

        :param context: Current context object.
        :returns: PAction for processor class.
        """
        raise NotImplementedError()
