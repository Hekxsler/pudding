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
            try:
                data = string_to_datatype(value)
            except TypeError as e:
                raise TypeError(
                    f"ERROR: Invalid data type {repr(value)} in line {lineno}"
                ) from e
            converted.append(data)
        return cls(lineno, name, tuple(converted))

    def get_compiled_patterns(
        self, context: Context, re_flag: ReFlag = ReFlag.NOFLAG
    ) -> Generator[re.Pattern[str], None, None]:
        """Return the combined patterns as a string.

        :param context: Context to resolve variables.
        :param re_flag: Regex flag when compiling expression.
        :returns: List of regex patterns, where each element is a possible pattern.
        """
        # If the pattern does not depend on runtime variables (Varname), cache
        # the compiled patterns per-instance to avoid re-compiling millions of
        # times for large inputs.
        contains_varname = any(isinstance(d, Varname) for d in self.values)
        if not contains_varname:
            cache = getattr(self, "_compiled_patterns", None)
            if cache is None:
                # build once and store compiled patterns for default flags
                patterns: list[re.Pattern[str]] = []
                buf = r""
                for data in self.values:
                    if isinstance(data, (String, Regex)):
                        value = data.pattern
                        buf += rf"({value.pattern})"
                    elif isinstance(data, Or):
                        patterns.append(re.compile(buf, re_flag))
                        buf = r""
                patterns.append(re.compile(buf, re_flag))
                self._compiled_patterns = {re_flag: tuple(patterns)}
                for p in patterns:
                    yield p
            else:
                for p in cache.get(re_flag, ()):  # type: ignore[attr-defined]
                    yield p
            return

        # fallback: pattern depends on Varname -> compile each time using context
        pattern = r""
        for data in self.values:
            if isinstance(data, (String, Regex)):
                value = data.pattern
                pattern += rf"({value.pattern})"
            if isinstance(data, Varname):
                value = context.get_var(data.value)
                pattern += rf"({value.pattern})"
            if isinstance(data, Or):
                yield re.compile(pattern, re_flag)
                pattern = r""
        yield re.compile(pattern, re_flag)

    def execute(self, context: Context) -> PAction:
        """Execute this token.

        :param context: Current context object.
        :returns: PAction for processor class.
        """
        raise NotImplementedError()
