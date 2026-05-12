"""Output function out.replace."""

import re

from ....datatypes import String
from ....processor import PAction
from ....processor.context import Context
from ..function import Function


class Replace(Function):
    """Class for `out.replace` function.

    Replaces the text of the last node in the given path.
    """

    min_args = 1
    max_args = 2

    match_re = re.compile(r"(out\.replace)\((.*)\)$")
    value_types = (String, String)

    def execute(self, context: Context) -> PAction:
        """Replace text of an element.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        new_value = None
        if self.get_value(1):
            new_value = context.replace_string_vars(self.get_string(1))
        context.writer.replace_element(
            context.replace_string_vars(self.get_string(0)), new_value
        )
        return PAction.CONTINUE
