"""Control function do.say."""

import re
import sys

from pudding.datatypes import String
from pudding.processor import PAction
from pudding.processor.context import Context

from ..function import Function


class Say(Function):
    """Class for `say` function.

    Prints the given string to stdout.
    """

    min_args = 1
    max_args = 1

    match_re = re.compile(r"(out\.say)\((.*)\)$")
    value_types = (String,)

    def execute(self, context: Context) -> PAction:
        """Print to stdout.

        :param context: Current context object.
        :returns: Returns PAction.CONTINUE for processor class.
        """
        sys.stdout.write(f"{self.get_replaced_string(0, context)}\n")
        return PAction.CONTINUE
