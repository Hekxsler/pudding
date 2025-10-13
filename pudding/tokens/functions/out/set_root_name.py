"""Output function out.set_root_name."""

import re

from ....writer.xml import Xml

from ...datatypes import String
from ....processor import PAction
from ....processor.context import Context
from .out import Out


class SetRootName(Out):
    """Class for `out.set_root_name` function."""

    max_args = 1

    match_re = re.compile(rf"(out\.set_root_name)\({String.regex}\)$")
    value_re = re.compile(rf"out\.set_root_name\(({String.regex})\)")
    value_types = (String,)

    def execute(self, context: Context) -> PAction:
        """Action for set_root_name function."""
        if isinstance(context.writer, Xml):
            context.writer.root_name = self.get_string(0).value
        return PAction.CONTINUE
