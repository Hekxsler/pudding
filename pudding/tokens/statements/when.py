"""When statement."""

import re

from ...processor import PAction
from ...processor.context import Context
from ..util import EXP_VAR
from .statement import MultiExpStatement


class When(MultiExpStatement):
    """Class for `when` statement."""

    match_re = re.compile(rf"(when)(?: {EXP_VAR})+\:$")
    value_re = re.compile(rf"when((?: {EXP_VAR})+)")

    def execute(self, context: Context) -> PAction:
        """Action for when statement."""
        for pattern in self.get_patterns(context):
            regex = re.compile(pattern)
            if context.reader.find(regex):
                return PAction.ENTER
        return PAction.NEXT


class IWhen(MultiExpStatement):
    """Class for `iwhen` statement."""

    match_re = re.compile(rf"(iwhen)(?: {EXP_VAR})+\:$")
    value_re = re.compile(rf"iwhen((?: {EXP_VAR})+)")

    def execute(self, context: Context) -> PAction:
        """Action for when statement."""
        for pattern in self.get_patterns(context):
            regex = re.compile(pattern, re.IGNORECASE)
            if context.reader.find(regex):
                return PAction.ENTER
        return PAction.NEXT
