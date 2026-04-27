"""Next statement."""

import re

from ...processor import PAction
from ...processor.context import Context
from .statement import Statement


class Next(Statement):
    """Class for `next` statement.

    Skip the current match and continue with the next match statement without jumping
    back to the top of the current grammar block. This function is rarely used and
    probably not what you want, unless it is for some performance-specific hacks.
    """

    match_re = re.compile(r"(next)$")
    value_re = re.compile(r"next")

    def execute(self, context: Context) -> PAction:
        """Continue with the next token of the grammar.

        :param context: Current context object.
        :returns: Returns PAction.NEXT for processor class.
        """
        return PAction.NEXT
