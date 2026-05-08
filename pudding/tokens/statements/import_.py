"""Import statement."""

import re
from typing import Self

from ...datatypes.util import string_to_datatype

from ...datatypes import String
from ...processor import PAction
from ...processor.context import Context
from .statement import Statement


class FromImport(Statement):
    """Class for `from ... import ...` statement."""

    match_re = re.compile(r"(from) +(.*) +import +(.*)$")
    value_types = (String, String)

    @classmethod
    def from_string(cls, string: str, lineno: int) -> Self:
        """Create FromImport statement from string.

        :param string: String containing the token.
        :param lineno: Line number of the token.
        """
        token_match = cls.match_re.match(string)
        if token_match is None:
            raise ValueError("Token not in given string.")
        name = token_match.group(1)
        values = [token_match.group(2), token_match.group(3)]
        return cls(lineno, name, tuple((string_to_datatype(v, lineno) for v in values)))

    def execute(self, context: Context) -> PAction:
        """Execute this token.

        :param context: Current context object.
        :raises SyntaxError: Can not be executed.
        """
        raise SyntaxError(
            f"Import statement not defined at top level in line {self.lineno}"
        )


class Import(Statement):
    """Class for `import` statement."""

    match_re = re.compile(r"(import) +(.*)$")
    value_types = (String,)

    def execute(self, context: Context) -> PAction:
        """Execute this token.

        :param context: Current context object.
        :raises SyntaxError: Can not be executed.
        """
        raise SyntaxError(
            f"Import statement not defined at top level in line {self.lineno}"
        )
