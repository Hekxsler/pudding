"""Define statement."""

import re

from ...processor import PAction
from ...processor.context import Context
from ...datatypes import Data, Or, Varname
from ..util import EXP_VAR
from .statement import Statement


class Define(Statement):
    """Class for `define` statement."""

    match_re = re.compile(rf"(define) {Varname.regex} *(?: *{EXP_VAR})+$")
    value_re = re.compile(rf"define ({Varname.regex}) *((?: *{EXP_VAR})+)")
    value_types = (Varname, Data)

    def get_pattern(self, context: Context) -> re.Pattern[str]:
        """Returns the combined patterns as a string.

        :param context: Context to resolve variables.
        :returns: Regex pattern.
        """
        pattern = r""
        for value in self.values[1:]:
            if isinstance(value, Or):
                raise SyntaxError(
                    f"Can not use '|' in define statement. (line {self.lineno})"
                )
            if isinstance(value, Varname):
                pattern += context.get_var(value.value).pattern
            else:
                pattern += value.pattern.pattern
        return re.compile(pattern)

    def execute(self, context: Context) -> PAction:
        """Set a variable.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        context.variables[self.values[0].value] = self.get_pattern(context)
        return PAction.CONTINUE
