"""Define statement."""

import re

from pudding.datatypes import Data, Or, Regex, String, Varname
from pudding.processor import PAction
from pudding.processor.context import Context

from .statement import MultiExpStatement


class Define(MultiExpStatement):
    """Class for `define` statement."""

    match_re = re.compile(r"(define) +(.*)$")
    value_types = (Varname, Data, ...)

    def execute(self, context: Context) -> PAction:
        """Set a variable.

        :param context: Current context object.
        :returns: PAction.CONTINUE
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

        context.variables[self.values[0].value] = pattern
        return PAction.CONTINUE
