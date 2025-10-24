"""Output function out.create."""

import re

from ....datatypes import String
from ....processor import PAction
from ....processor.context import Context
from ..function import OPTIONAL_STRING
from .out import Out


class Create(Out):
    """Class for `out.create` function.

    Creates the leaf node (and attributes) in the given path, regardless of whether or
    not it already exists. In other words, using this function twice will lead to
    duplicates. If the given path contains multiple elements, the parent nodes are only
    created if they do not yet exist. If the second argument is given, the new node is
    also assigned the string as data.
    """

    match_re = re.compile(rf"(out\.create)\({String.regex}{OPTIONAL_STRING}\)$")
    value_re = re.compile(rf"out\.create\(({String.regex}){OPTIONAL_STRING}\)")
    value_types = (String, String)

    def execute(self, context: Context) -> PAction:
        """Create an element always.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        value = None
        if self.get_value(1):
            value = context.replace_string_vars(self.get_string(1))
        context.writer.create_element(
            context.replace_string_vars(self.get_string(0)),
            value,
        )
        return PAction.CONTINUE
