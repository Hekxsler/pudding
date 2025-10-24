"""Output function out.remove."""

import re

from ....processor import PAction
from ....processor.context import Context
from ....datatypes import String
from .out import Out


class Remove(Out):
    """Class for `out.remove` function.

    Deletes the last node in the given path.
    """

    match_re = re.compile(rf"(out\.remove)\({String.regex}\)$")
    value_re = re.compile(rf"out\.remove\(({String.regex})\)")
    value_types = (String,)

    def execute(self, context: Context) -> PAction:
        """Delete an element.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        context.writer.delete_element(context.replace_string_vars(self.get_string(0)))
        return PAction.CONTINUE
