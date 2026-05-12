"""Grammar call."""

import re

from pudding.datatypes import Varname

from .function import Function


class GrammarCall(Function):
    """Class for a grammar call."""

    match_re = re.compile(rf"({Varname.regex})\((.*)\)$")
    value_types = tuple()
