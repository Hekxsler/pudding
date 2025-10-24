"""Control function do.fail."""

import re
from typing import NoReturn

from ....datatypes.string import String
from ....processor.context import Context
from .do import Do


class Fail(Do):
    """Class for `do.fail` function.

    Takes exactly one argument with a string printed to stdout on execution.
    """

    min_args = 1
    max_args = 1

    match_re = re.compile(rf"(do\.fail)\({String.regex}\)$")
    value_re = re.compile(rf"do\.fail\(({String.regex})\)")
    value_types = (String,)

    def execute(self, context: Context) -> NoReturn:
        """Immediately terminate parsing with an error.

        :param context: Current context object.
        :raises RuntimeError: Error with given message.
        """
        raise RuntimeError(context.replace_string_vars(self.get_string(0)))
