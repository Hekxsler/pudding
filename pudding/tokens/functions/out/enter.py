"""Output function out.enter."""

import re

from ....datatypes import String
from ....processor import PAction
from ....processor.context import Context
from ..function import OPTIONAL_STRING
from .out import Out


class Enter(Out):
    """Class for `out.enter` function.

    Creates the nodes in the given path if they do not already exist and
    selects the last node. Therefore the PATH of all subsequent function calls is
    relative to the selected node until the end of the match block is reached.
    """

    match_re = re.compile(rf"(out\.enter)\({String.regex}{OPTIONAL_STRING}\)$")
    value_re = re.compile(rf"out\.enter\(({String.regex}{OPTIONAL_STRING})\)")
    value_types = (String, String)

    def execute(self, context: Context) -> PAction:
        """Action for enter function."""
        context.writer.enter_path(
            self.get_replaced_string(0, context),
            self.get_repl_opt_string(1, context),
        )
        return PAction.CONTINUE
