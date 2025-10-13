"""Control function do.fail."""

import re
from typing import NoReturn

from ...datatypes import String
from ....processor.context import Context
from .do import Do


class Fail(Do):
    """Class for `do.fail` function.

    Immediately terminates parsing with an error. Takes exactly one argument
    with a string printed to stdout on execution.
    """

    min_args = 1
    max_args = 1

    match_re = re.compile(rf"(do\.fail)\({String.regex}\)$")
    value_re = re.compile(rf"do\.fail\(({String.regex})\)")
    value_types = (String,)

    def execute(self, context: Context) -> NoReturn:
        """Action of fail function."""
        raise RuntimeError(self.get_replaced_string(0, context))
