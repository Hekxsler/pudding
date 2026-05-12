"""Output function out.add_attribute."""

import re

from pudding.datatypes import String
from pudding.processor import PAction
from pudding.processor.context import Context

from ..function import Function


class AddAttribute(Function):
    """Class for `out.add_attribute` function.

    Adds the attribute with the given name and value to the node at the given path.
    """

    min_args = 3
    max_args = 3

    match_re = re.compile(r"(out\.add_attribute)\((.*)\)$")
    value_types = (String, String, String)

    def execute(self, context: Context) -> PAction:
        """Add an attribute.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        context.writer.add_attribute(
            self.get_replaced_path(0, context),
            self.get_replaced_string(1, context),
            self.get_replaced_string(2, context),
        )
        return PAction.CONTINUE
