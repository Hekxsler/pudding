"""Output function out.add_attribute."""

import re

from ...datatypes import String
from ....processor import PAction
from ....processor.context import Context
from .out import Out


class AddAttribute(Out):
    """Class for `out.add_attribute` function.

    Adds the attribute with the given name and value to the node at the given path.
    """

    min_args = 3
    max_args = 3

    match_re = re.compile(
        rf"(out\.add_attribute)\({String.regex}, *{String.regex}, *{String.regex}\)$"
    )
    value_re = re.compile(
        rf"out\.add_attribute\(({String.regex}), *({String.regex}), *({String.regex})\)"
    )
    value_types = (String, String, String)

    def execute(self, context: Context) -> PAction:
        """Action for add_attribute function."""
        context.writer.add_attribute(
            self.get_replaced_string(0, context),
            self.get_replaced_string(1, context),
            self.get_replaced_string(2, context),
        )
        return PAction.CONTINUE
