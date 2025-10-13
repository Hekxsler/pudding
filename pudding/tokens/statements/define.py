"""Define statement."""

import re

from ...processor import PAction
from ...processor.context import Context
from ..datatypes import Data, Varname
from ..util import EXP_VAR
from .statement import Statement


class Define(Statement):
    """Class for `define` statement."""

    match_re = re.compile(rf"(define) {Varname.regex} *{EXP_VAR}$")
    value_re = re.compile(rf"define ({Varname.regex}) *({EXP_VAR})")
    value_types = (Varname, Data)

    def execute(self, context: Context) -> PAction:
        """Action for define statement."""
        raise SyntaxError(
            f"Define statement not defined at top level in line {self.lineno}"
        )
