"""Utility constants and functions for parsing."""

import re

from ..datatypes import Regex, String, Varname, Or

INDENTATION_RE = re.compile(r"^(\s|\t)+")

EXPRESSION_RE = rf"(?:{Regex.regex}|{String.regex}|{Or.regex})"
EXP_VAR = rf"(?:{EXPRESSION_RE}|{Varname.regex})"
