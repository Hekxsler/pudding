"""Control function do.say."""

import re
import sys
import warnings

from ...datatypes.string import String
from ...processor import PAction
from ...processor.context import Context
from .function import Function


class Say(Function):
    """Class for `say` function.

    Prints the given string to stdout.
    """

    min_args = 1
    max_args = 1

    match_re = re.compile(rf"(say)\({String.regex}\)$")
    value_re = re.compile(rf"say\(({String.regex})\)")
    value_types = (String,)

    def execute(self, context: Context) -> PAction:
        """Print to stdout.

        :param context: Current context object.
        :returns: Returns PAction.CONTINUE for processor class.
        """
        message = context.replace_string_vars(self.get_string(0))
        sys.stdout.write(f"{message}\n")
        return PAction.CONTINUE
