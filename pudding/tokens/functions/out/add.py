"""Output function out.add."""

import re

from ....datatypes import String
from ....processor import PAction
from ....processor.context import Context
from ..function import OPTIONAL_STRING
from .out import Out


class Add(Out):
    """Class for `out.add` function.

    Appends the string value to the text of the existing node if it already exists.
    Otherwise it creates a new node.
    """

    match_re = re.compile(rf"(out\.add)\({String.regex}{OPTIONAL_STRING}\)$")
    value_re = re.compile(rf"out\.add\(({String.regex}){OPTIONAL_STRING}\)")
    value_types = (String, String)

    def execute(self, context: Context) -> PAction:
        """Add an element.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        value = None
        if self.get_value(1):
            value = context.replace_string_vars(self.get_string(1))
        context.writer.add_element(
            context.replace_string_vars(self.get_string(0)), value
        )
        return PAction.CONTINUE
