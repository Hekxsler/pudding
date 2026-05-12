"""Fail statement."""

import re
from typing import NoReturn

from pudding.datatypes import String
from pudding.processor.context import Context

from .statement import Statement


class Fail(Statement):
    """Class for `fail` statement.

    Takes exactly one argument with a string printed to stdout on execution.
    """

    match_re = re.compile(r"(fail) *(.*)$")
    value_types = (String,)

    def execute(self, context: Context) -> NoReturn:
        """Immediately terminate parsing with an error.

        :param context: Current context object.
        :raises RuntimeError: Error with given message.
        """
        if len(self.values) == 1:
            raise RuntimeError(self.get_replaced_string(0, context))
        raise RuntimeError(f"Fail statement in line {self.lineno}.")
