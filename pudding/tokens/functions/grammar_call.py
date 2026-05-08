"""Grammar call."""

import re

from ...datatypes.varname import Varname
from .function import Function


class GrammarCall(Function):
    """Class for a grammar call."""

    match_re = re.compile(rf"({Varname.regex})\((.*)\)$")
    value_types = tuple()
