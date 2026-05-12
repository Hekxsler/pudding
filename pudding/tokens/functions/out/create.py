"""Output function out.create."""

import re

from pudding.datatypes import String
from pudding.processor import PAction
from pudding.processor.context import Context

from ..function import Function


class Create(Function):
    """Class for `out.create` function.

    Creates the leaf node (and attributes) in the given path, regardless of whether or
    not it already exists. In other words, using this function twice will lead to
    duplicates. If the given path contains multiple elements, the parent nodes are only
    created if they do not yet exist. If the second argument is given, the new node is
    also assigned the string as data.
    """

    min_args = 1
    max_args = 2

    match_re = re.compile(r"(out\.create)\((.*)\)$")
    value_types = (String, String)

    def execute(self, context: Context) -> PAction:
        """Create an element always.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        context.writer.create_element(
            self.get_replaced_string(0, context),
            self.get_optional_replaced_string(1, context),
        )
        return PAction.CONTINUE
