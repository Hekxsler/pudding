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
        context.writer.replace_element(
            self.get_replaced_string(0, context), self.get_repl_opt_string(1, context)
        )
        return PAction.CONTINUE
