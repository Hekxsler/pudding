"""Grammar call."""

import re
from typing import NoReturn

from ...datatypes.varname import Varname
from ...processor.context import Context
from .function import Function


class GrammarCall(Function):
    """Class for a grammar call."""

    min_args = 0
    max_args = 0

    match_re = re.compile(rf"({Varname.regex})\(\)$")
    value_re = re.compile(rf"{Varname.regex}\(\)")
    value_types = (Varname,)

    def execute(self, context: Context) -> NoReturn:
        """Execute this token.
        
        :param context: Current context object.
        :raises RuntimeError: This token can not be executed.
        """
        raise RuntimeError
