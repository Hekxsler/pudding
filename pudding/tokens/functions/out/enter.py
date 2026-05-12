"""Output function out.enter."""

import re

from pudding.datatypes import String
from pudding.processor import PAction
from pudding.processor.context import Context

from ..function import Function


class Enter(Function):
    """Class for `out.enter` function.

    Creates the nodes in the given path if they do not already exist and
    selects the last node. Therefore the PATH of all subsequent function calls is
    relative to the selected node until the end of the match block is reached.
    """

    min_args = 1
    max_args = 2

    match_re = re.compile(r"(out\.enter)\((.*)\)$")
    value_types = (String, String)

    def execute(self, context: Context) -> PAction:
        """Enter a node and create it if it does not exist.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        context.writer.enter_path(
            self.get_replaced_string(0, context),
            self.get_optional_replaced_string(1, context),
        )
        return PAction.CONTINUE
