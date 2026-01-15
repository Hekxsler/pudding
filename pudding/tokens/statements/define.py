"""Define statement."""

import re

from ...datatypes import Data, Varname
from ...datatypes.or_ import Or
from ...datatypes.regex import Regex
from ...datatypes.string import String
from ...processor import PAction
from ...processor.context import Context
from ..util import EXP_VAR
from .statement import Statement


class Define(Statement):
    """Class for `define` statement."""

    match_re = re.compile(rf"(define) +{Varname.regex} +(?: +{EXP_VAR})+$")
    value_re = re.compile(rf"define +({Varname.regex}) +((?: +{EXP_VAR})+)")
    value_types = (Varname, Data)

    def get_patterns(self, context: Context) -> str:
        """Return the combined patterns as a string.

        :param context: Context to resolve variables.
        :param re_flag: Regex flag when compiling expression.
        :returns: List of regex patterns, where each element is a possible pattern.
        """
        pattern = r""
        for data in self.values[1:]:
            if isinstance(data, (String, Regex)):
                pattern += data.re_pattern
            elif isinstance(data, Varname):
                pattern += context.get_var(data)
            elif isinstance(data, Or):
                msg = "Define statement can't contain Or-character."
                raise SyntaxError(f"{msg} (line {self.lineno})")
        return pattern

    def execute(self, context: Context) -> PAction:
        """Set a variable.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        context.variables[self.values[0].value] = self.get_patterns(context)
        return PAction.CONTINUE
