"""Output function out.open."""

import re

from ....datatypes import String
from ....processor import PAction
from ....processor.context import Context
from ..function import OPTIONAL_STRING
from .out import Out


class Open(Out):
    """Class for `out.open` function.

    Like out.create(), but also selects the addressed node, such that the PATH of all
    subsequent function calls is relative to the selected node until the end of the
    match block is reached.
    """

    match_re = re.compile(rf"(out\.open)\({String.regex}{OPTIONAL_STRING}\)$")
    value_re = re.compile(rf"out\.open\(({String.regex}){OPTIONAL_STRING}\)")
    value_types = (String, String)

    def execute(self, context: Context) -> PAction:
        """Create and enter a node.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        value = None
        if self.get_value(1):
            value = context.replace_string_vars(self.get_string(1))
        context.writer.open_path(
            context.replace_string_vars(self.get_string(0)), value
        )
        return PAction.CONTINUE
