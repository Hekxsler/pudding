"""Skip statement."""

import re

from pudding.processor import PAction
from pudding.processor.context import Context

from ..util import EXP_VAR
from .match import Match, IMatch


class Skip(Match):
    """Class for `skip` statement."""

    match_re = re.compile(rf"(skip)(?: {EXP_VAR})+$")
    value_re = re.compile(rf"skip((?: {EXP_VAR})+)")

    def execute(self, context: Context) -> PAction:
        action = super().execute(context)
        if action == PAction.ENTER:
            return PAction.RESTART
        return PAction.NEXT

class ISkip(IMatch):
    """Class for `skip` statement."""

    match_re = re.compile(rf"(iskip)(?: {EXP_VAR})+$")
    value_re = re.compile(rf"iskip((?: {EXP_VAR})+)")

    def execute(self, context: Context) -> PAction:
        action = super().execute(context)
        if action == PAction.ENTER:
            return PAction.RESTART
        return PAction.NEXT
