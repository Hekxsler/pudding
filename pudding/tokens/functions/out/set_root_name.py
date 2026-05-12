"""Output function out.set_root_name."""

import re

from pudding.datatypes import String
from pudding.processor import PAction
from pudding.processor.context import Context

from ..function import Function


class SetRootName(Function):
    """Class for `out.set_root_name` function."""

    min_args = 1
    max_args = 1

    match_re = re.compile(r"(out\.set_root_name)\((.*)\)$")
    value_types = (String,)

    def execute(self, context: Context) -> PAction:
        """Set tag of root element.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        context.writer.root_name = self.get_string(0).value
        return PAction.CONTINUE
