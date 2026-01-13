"""Return statement."""

import re

from ...processor import PAction
from ...processor.context import Context
from .statement import Statement


class Return(Statement):
    """Class for `return` statement.

    Immediately leave the current grammar block and return to the calling function.
    When used at the top level (i.e. in the input grammar), stop parsing.
    """

    match_re = re.compile(r"(return)$")
    value_re = re.compile(r"return")

    def execute(self, context: Context) -> PAction:
        """Immediately leave the current grammar.

        :param context: Current context object.
        :returns: Returns PAction.EXIT for processor class.
        """
        return PAction.EXIT
