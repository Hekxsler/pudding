"""Control function do.say."""

import re

from ...datatypes import String
from ....processor import PAction
from ....processor.context import Context
from .do import Do


class Say(Do):
    """Class for `do.say` function.

    Prints the given string to stdout.
    """

    min_args = 1
    max_args = 1

    match_re = re.compile(rf"(do\.say)\({String.regex}\)$")
    value_re = re.compile(rf"do\.say\(({String.regex})\)")
    value_types = (String,)

    def execute(self, context: Context) -> PAction:
        """Action for say function."""
        print(self.get_replaced_string(0, context))
        return PAction.CONTINUE
