"""Import statement."""

import re

from ...processor import PAction
from ...processor.context import Context
from ..datatypes import String
from .statement import Statement


class FromImport(Statement):
    """Class for `from ... import ...` statement."""

    match_re = re.compile(rf"(from) {String.regex} import {String.regex}$")
    value_re = re.compile(rf"from ({String.regex}) import ({String.regex})")
    value_types = (String , String)

    def execute(self, context: Context) -> PAction:
        """Action for import statement."""
        raise SyntaxError(
            f"Import statement not defined at top level in line {self.lineno}"
        )


class Import(Statement):
    """Class for `import` statement."""

    match_re = re.compile(rf"(import) {String.regex}$")
    value_re = re.compile(rf"import ({String.regex})")
    value_types = (String,)

    def execute(self, context: Context) -> PAction:
        """Action for import statement."""
        raise SyntaxError(
            f"Import statement not defined at top level in line {self.lineno}"
        )

