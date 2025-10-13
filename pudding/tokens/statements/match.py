"""Match statement."""

import re

from ...processor import PAction
from ...processor.context import Context
from ..util import EXP_VAR
from .statement import MultiExpStatement


class Match(MultiExpStatement):
    """Class for `match` statement."""

    match_re = re.compile(rf"(match)(?: {EXP_VAR})+\:$")
    value_re = re.compile(rf"match((?: {EXP_VAR})+)")

    def execute(self, context: Context) -> PAction:
        """Action for match statement."""
        for pattern in self.get_patterns(context):
            regex = re.compile(pattern)
            if context.reader.match(regex):
                return PAction.RESTART
        return PAction.CONTINUE


class IMatch(MultiExpStatement):
    """Class for `imatch` statement."""

    match_re = re.compile(rf"(imatch)(?: {EXP_VAR})+\:$")
    value_re = re.compile(rf"imatch((?: {EXP_VAR})+)")

    def execute(self, context: Context) -> PAction:
        """Action for imatch statement."""
        for pattern in self.get_patterns(context):
            regex = re.compile(pattern, re.IGNORECASE)
            if context.reader.match(regex):
                return PAction.RESTART
        return PAction.CONTINUE
