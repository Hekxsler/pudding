"""Module defining statements."""

import re
from typing import Self, TypeVar

from ..util import EXP_VAR

from ..datatypes import Data, Or, Varname

from ...processor import PAction
from ...processor.context import Context
from ..token import Token

_T = TypeVar("_T", bound=tuple[Data, ...])


class Statement(Token):
    """Base class for a statement."""

    @classmethod
    def from_string(cls, string: str, lineno: int) -> Self:
        """Create Statement object from string.

        :param string: String containing the statement.
        """
        statement = cls.match_re.search(string)
        if statement is None:
            raise ValueError("Statement not in given string.")
        name = statement.group(1)
        value_match = cls.value_re.search(statement.group(0))
        if value_match is None:
            raise ValueError("No values in statement.")
        values = tuple([str(x) for x in value_match.groups() if x is not None])
        return cls(lineno, name, values)

    def execute(self, context: Context) -> PAction:
        """Function for context changing actions."""
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
        return cls(lineno, name, tuple(values))

    def get_patterns(self, context: Context) -> list[str]:
        """Returns the combined patterns as a string.

        :param context: Context to resolve variables.
        :returns: List of regex patterns.
        """
        patterns = [r""]
        for value in self.values:
            if isinstance(value, Or):
                patterns.append(r"")
                continue
            if isinstance(value, Varname):
                value = context.get_var(value.value)
            else:
                value = value.pattern
            patterns[-1] += rf"({value.pattern})"
        return patterns

    def execute(self, context: Context) -> PAction:
        """Function for context changing actions."""
        raise NotImplementedError()
