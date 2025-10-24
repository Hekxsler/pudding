"""Module defining statements."""

import re
from re import RegexFlag as ReFlag
from typing import Generator, Self, TypeVar

from ...datatypes.regex import Regex

from ...datatypes.string import String

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
            data = string_to_datatype(value, lineno)
            converted.append(data)
        return cls(lineno, name, tuple(converted))

    def get_patterns(self, context: Context) -> Generator[str, None, None]:
        """Return the combined patterns as a string.

        :param context: Context to resolve variables.
        :param re_flag: Regex flag when compiling expression.
        :returns: List of regex patterns, where each element is a possible pattern.
        """
        pattern = r""
        for data in self.values:
            if isinstance(data, (String, Regex)):
                pattern += rf"({data.re_pattern})"
            elif isinstance(data, Varname):
                pattern += rf"({context.get_var(data)})"
            elif isinstance(data, Or):
                yield pattern
                pattern = r""
        yield pattern

    def get_compiled_patterns(
        self, context: Context, re_flag: ReFlag = ReFlag.NOFLAG
    ) -> Generator[re.Pattern[str], None, None]:
        """Return the combined patterns as a string.

        :param context: Context to resolve variables.
        :param re_flag: Regex flag when compiling expression.
        :returns: List of regex patterns, where each element is a possible pattern.
        """
        for pattern in self.get_patterns(context):
            yield re.compile(pattern, re_flag)

    def execute(self, context: Context) -> PAction:
        """Execute this token.

        :param context: Current context object.
        :returns: PAction for processor class.
        """
        raise NotImplementedError()
