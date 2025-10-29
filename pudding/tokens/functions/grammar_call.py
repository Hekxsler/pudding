"""Grammar call."""

import re

from ...datatypes.varname import Varname
from .function import Function


class GrammarCall(Function):
    """Class for a grammar call."""

    min_args = 0
    max_args = 0

    match_re = re.compile(rf"({Varname.regex})\(\)$")
    value_re = re.compile(rf"{Varname.regex}\(\)")
    value_types = (Varname,)
