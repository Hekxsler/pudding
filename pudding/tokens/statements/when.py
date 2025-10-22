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
        """Search a pattern to the content ahead.

        :param context: Current context object.
        :returns: PAction.ENTER if pattern matches, else PAction.NEXT.
        """
        for pattern in self.get_compiled_patterns(context):
            if context.reader.find(pattern):
                return PAction.ENTER
        return PAction.NEXT


class IWhen(MultiExpStatement):
    """Class for `iwhen` statement."""

    match_re = re.compile(rf"(iwhen)(?: {EXP_VAR})+\:$")
    value_re = re.compile(rf"iwhen((?: {EXP_VAR})+)")

    def execute(self, context: Context) -> PAction:
        """Search a pattern to the content ahead (case-insensitive).

        :param context: Current context object.
        :returns: PAction.ENTER if pattern matches, else PAction.NEXT.
        """
        for pattern in self.get_compiled_patterns(context, re.RegexFlag.IGNORECASE):
            if context.reader.find(pattern):
                return PAction.ENTER
        return PAction.NEXT
