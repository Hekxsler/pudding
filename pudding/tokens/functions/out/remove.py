"""Output function out.remove."""

import re

from pudding.datatypes import String
from pudding.processor import PAction
from pudding.processor.context import Context

from ..function import Function


class Remove(Function):
    """Class for `out.remove` function.

    Deletes the last node in the given path.
    """

    min_args = 1
    max_args = 1

    match_re = re.compile(r"(out\.remove)\((.*)\)$")
    value_types = (String,)

    def execute(self, context: Context) -> PAction:
        """Delete an element.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        context.writer.delete_element(self.get_replaced_string(0, context))
        return PAction.CONTINUE
