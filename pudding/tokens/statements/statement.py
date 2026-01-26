"""Module defining statements."""

import re
from re import RegexFlag as ReFlag
from types import EllipsisType
from typing import Generator, Self

from ...datatypes import Data, Or, Varname, string_to_datatype
from ...datatypes.regex import Regex
from ...datatypes.string import String
from ...processor.context import Context
from ..token import Token, ValueType
from ..util import EXP_VAR


class Statement(Token):
    """Base class for a statement."""

    value_types = ()


class MultiExpStatement(Statement):
    """Base class for a statement with multiple expressions."""

    value_types: tuple[*tuple[ValueType, ...], EllipsisType] = (Data, ...)

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
        for t in cls.value_types:
            if isinstance(t, EllipsisType):
                break
            yield t
        yield cls.value_types[-2]

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
