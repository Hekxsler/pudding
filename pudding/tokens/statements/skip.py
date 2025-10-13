"""Skip statement."""

import re

from ..util import EXP_VAR
from .match import Match


class Skip(Match):
    """Class for `skip` statement."""

    match_re = re.compile(rf"(skip)(?: {EXP_VAR})+$")
    value_re = re.compile(rf"skip((?: {EXP_VAR})+)")
