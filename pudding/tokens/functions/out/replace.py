"""Output function out.replace."""

import re

from ....datatypes import String
from ....processor import PAction
from ....processor.context import Context
from ..function import OPTIONAL_STRING
from .out import Out


class Replace(Out):
    """Class for `out.replace` function.

    Replaces the text of the last node in the given path.
    """

    match_re = re.compile(rf"(out\.replace)\({String.regex}{OPTIONAL_STRING}\)$")
    value_re = re.compile(rf"out\.replace\(({String.regex}){OPTIONAL_STRING}\)")
    value_types = (String, String)

    def execute(self, context: Context) -> PAction:
        """Replace text of an element.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        value = None
        if self.get_value(1):
            value = context.replace_string_vars(self.get_string(1))
        context.writer.replace_element(
            context.replace_string_vars(self.get_string(0)), value
        )
        return PAction.CONTINUE
