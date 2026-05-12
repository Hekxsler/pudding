"""Match statement."""

import re
from typing import Callable

from pudding.processor import PAction
from pudding.processor.context import Context

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

    match_re = re.compile(r"(match) +(.*)\:$")
    re_flag = re.RegexFlag.NOFLAG

    execute = enter_on_match(MultiExpStatement.execute)


class IMatch(MultiExpStatement):
    """Class for `imatch` statement."""

    match_re = re.compile(r"(imatch) +(.*)\:$")
    re_flag = re.RegexFlag.IGNORECASE

    execute = enter_on_match(MultiExpStatement.execute)
