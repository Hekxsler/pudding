"""Output function out.add."""

import re

from pudding.datatypes import String
from pudding.processor import PAction
from pudding.processor.context import Context

from ..function import Function


class Add(Function):
    """Class for `out.add` function.

    Appends the string value to the text of the existing node if it already exists.
    Otherwise it creates a new node.
    """

    min_args = 1
    max_args = 2

    match_re = re.compile(r"(out\.add)\((.*)\)$")
    value_types = (String, String)

    def execute(self, context: Context) -> PAction:
        """Add an element.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        context.writer.add_element(
            self.get_replaced_string(0, context),
            self.get_optional_replaced_string(1, context),
        )
        return PAction.CONTINUE
