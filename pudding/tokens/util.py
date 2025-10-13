"""Utility constants and functions for parsing."""

import re
from .datatypes import Regex, String, Varname

INDENTATION_RE = re.compile(r"^(\s|\t)+")

STRING_VAR_RE = r"([^\d]?\$(\d+)[^\$]?)"
# match chars before and after to not match $1 and $10 when replacing $1

EXPRESSION_RE = rf"(?:{Regex.regex}|{String.regex}|\|)"
EXP_VAR = rf"(?:{EXPRESSION_RE}|{Varname.regex})"
