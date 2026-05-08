"""When statement."""

import re
from typing import Callable

from ...processor import PAction
from ...processor.context import Context
from .statement import MultiExpStatement


def enter_on_find(_: Callable[..., PAction]) -> Callable[..., PAction]:
    """Enter code block when pattern is found."""

    def wrapper(self: "When | IWhen", context: Context) -> PAction:
        for pattern in self.get_compiled_patterns(context, re_flag=self.re_flag):
            if context.reader.find(pattern):
                return PAction.ENTER
        return PAction.NEXT

    return wrapper


class When(MultiExpStatement):
    """Class for `when` statement."""

    match_re = re.compile(r"(when) (.*)\:$")
    re_flag = re.RegexFlag.NOFLAG

    execute = enter_on_find(MultiExpStatement.execute)


class IWhen(MultiExpStatement):
    """Class for `iwhen` statement."""

    match_re = re.compile(r"(iwhen) (.*)\:$")
    re_flag = re.RegexFlag.IGNORECASE

    execute = enter_on_find(MultiExpStatement.execute)
