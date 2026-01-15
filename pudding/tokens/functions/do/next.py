"""Control function do.next."""

import re
import warnings

from ....processor import PAction
from ....processor.context import Context
from .do import Do


class Next(Do):
    """Class for `do.next` function.

    Skip the current match and continue with the next match statement without jumping
    back to the top of the current grammar block. This function is rarely used and
    probably not what you want, unless it is for some performance-specific hacks.
    """

    match_re = re.compile(r"(do\.next)\(\)$")
    value_re = re.compile(r"do\.next\(\)")

    def execute(self, context: Context) -> PAction:
        """Continue with the next token of the grammar.

        :param context: Current context object.
        :returns: Returns PAction.NEXT for processor class.
        """
        warnings.warn(
            "The function 'do.next()' is deprecated. Use statement 'next' instead.",
            DeprecationWarning,
        )
        return PAction.NEXT
