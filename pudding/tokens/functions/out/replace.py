"""Output function out.replace."""

import re

from pudding.datatypes import String
from pudding.processor import PAction
from pudding.processor.context import Context

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
        context.writer.replace_element(
            self.get_replaced_string(0, context),
            self.get_optional_replaced_string(1, context),
        )
        return PAction.CONTINUE
