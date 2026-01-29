"""Fail statement."""

import re
from typing import NoReturn

from ...datatypes.string import String
from ...processor.context import Context
from .statement import Statement


class Fail(Statement):
    """Class for `fail` statement.

    Takes exactly one argument with a string printed to stdout on execution.
    """

    match_re = re.compile(rf"(fail)(?: +{String.regex})?$")
    value_re = re.compile(rf"fail(?: +({String.regex}))?")
    value_types = (String,)

    def execute(self, context: Context) -> NoReturn:
        """Immediately terminate parsing with an error.

        :param context: Current context object.
        :raises RuntimeError: Error with given message.
        """
        if len(self.values) == 1:
            raise RuntimeError(context.replace_string_vars(self.get_string(0)))
        raise RuntimeError(f"Fail statement in line {self.lineno}.")
