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
        """Match a pattern to the content ahead.

        :param context: Current context object.
        :returns: PAction.ENTER if pattern matches, else PAction.NEXT.
        """
        patterns = (re.compile(p) for p in self.get_patterns(context))
        for pattern in patterns:
            if context.reader.match(pattern):
                return PAction.ENTER
        return PAction.NEXT


class IMatch(MultiExpStatement):
    """Class for `imatch` statement."""

    match_re = re.compile(rf"(imatch)(?: {EXP_VAR})+\:$")
    value_re = re.compile(rf"imatch((?: {EXP_VAR})+)")

    def execute(self, context: Context) -> PAction:
        """Match a pattern to the content ahead (case-insensitive).

        :param context: Current context object.
        :returns: PAction.ENTER if pattern matches, else PAction.NEXT.
        """
        for pattern in self.get_patterns(context):
            regex = re.compile(pattern, re.IGNORECASE)
            if context.reader.match(regex):
                return PAction.ENTER
        return PAction.NEXT
