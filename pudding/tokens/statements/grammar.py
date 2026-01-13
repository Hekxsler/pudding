"""Grammar statement."""

import re

from ...processor import PAction
from ...processor.context import Context
from ...datatypes import Varname
from .statement import Statement


class Grammar(Statement):
    """Class for `grammar` statement."""

    match_re = re.compile(rf"(grammar) {Varname.regex}(?:\({Varname.regex}\))?\:$")
    value_re = re.compile(rf"grammar ({Varname.regex})(?:\(({Varname.regex})\))?")
    value_types = (Varname, Varname)

    def execute(self, context: Context) -> PAction:
        """Execute this token.

        :param context: Current context object.
        :raises SyntaxError: Can not be executed.
        """
        raise SyntaxError(f"Grammar not defined at top level in line {self.lineno}")
