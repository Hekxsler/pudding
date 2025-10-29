"""Module defining statements."""

import re
from re import RegexFlag as ReFlag
from typing import Generator

from ...datatypes import Data, Or, Varname
from ...datatypes.regex import Regex
from ...datatypes.string import String
from ...processor.context import Context
from ..token import Token


class Statement(Token):
    """Base class for a statement."""


class MultiExpStatement(Statement):
    """Base class for a statement with multiple expressions."""

    value_types = (Data,)

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
