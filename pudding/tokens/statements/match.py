"""Match statement."""

import re
from typing import Callable

from ...processor import PAction
from ...processor.context import Context
from ..util import EXP_VAR
from .statement import MultiExpStatement


def enter_on_match(_: Callable[..., PAction]) -> Callable[..., PAction]:
    """Enter code block when text matches."""
    def wrapper(self: "Match | IMatch", context: Context) -> PAction:
        for pattern in self.get_compiled_patterns(context, re_flag=self.re_flag):
            if context.reader.match(pattern):
                return PAction.ENTER
        return PAction.NEXT

    return wrapper


class Match(MultiExpStatement):
    """Class for `match` statement."""

    match_re = re.compile(rf"(match)(?: +{EXP_VAR})+\:$")
    value_re = re.compile(rf"match((?: +{EXP_VAR})+)")
    re_flag = re.RegexFlag.NOFLAG

    execute = enter_on_match(MultiExpStatement.execute)


class IMatch(MultiExpStatement):
    """Class for `imatch` statement."""

    match_re = re.compile(rf"(imatch)(?: +{EXP_VAR})+\:$")
    value_re = re.compile(rf"imatch((?: +{EXP_VAR})+)")
    re_flag = re.RegexFlag.IGNORECASE

    execute = enter_on_match(MultiExpStatement.execute)
