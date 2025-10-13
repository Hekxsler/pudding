"""Grammar statement."""

import re

from ...processor import PAction
from ...processor.context import Context
from ..datatypes import Varname
from .statement import Statement


class Grammar(Statement):
    """Class for `grammar` statement."""

    match_re = re.compile(r"(grammar) \w+(?:\(\w+\))?\:$")
    value_re = re.compile(r"grammar (\w+)(?:\((\w+)\))?")
    value_types = (Varname, Varname)

    def execute(self, context: Context) -> PAction:
        """Action for grammar statement."""
        raise SyntaxError(f"Grammar not defined at top level in line {self.lineno}")
