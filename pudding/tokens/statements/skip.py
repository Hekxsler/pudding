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
        """Match a pattern to the content ahead and skip it.

        :param context: Current context object.
        :returns: PAction.ENTER if pattern matches, else PAction.NEXT.
        """
        action = super().execute(context)
        if action == PAction.ENTER:
            return PAction.RESTART
        return PAction.NEXT


class ISkip(IMatch):
    """Class for `iskip` statement."""

    match_re = re.compile(rf"(iskip)(?: {EXP_VAR})+$")
    value_re = re.compile(rf"iskip((?: {EXP_VAR})+)")

    def execute(self, context: Context) -> PAction:
        """Match a pattern to the content ahead and skip it (case-insensitive).

        :param context: Current context object.
        :returns: PAction.ENTER if pattern matches, else PAction.NEXT.
        """
        action = super().execute(context)
        if action == PAction.ENTER:
            return PAction.RESTART
        return PAction.NEXT
