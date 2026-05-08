"""When statement."""

import re
from typing import Callable

from ...processor import PAction
from ...processor.context import Context
from ..util import EXP_VAR
from .statement import MultiExpStatement


def enter_on_find(method: Callable[..., PAction]) -> Callable[..., PAction]:
    def wrapper(self: "When | IWhen", context: Context) -> PAction:
        for pattern in self.get_compiled_patterns(context, re_flag=self.re_flag):
            if context.reader.find(pattern):
                return PAction.ENTER
        return PAction.NEXT

    return wrapper


class When(MultiExpStatement):
    """Class for `when` statement."""

    match_re = re.compile(rf"(when)(?: +{EXP_VAR})+\:$")
    value_re = re.compile(rf"when((?: +{EXP_VAR})+)")
    re_flag = re.RegexFlag.NOFLAG

    execute = enter_on_find(MultiExpStatement.execute)


class IWhen(MultiExpStatement):
    """Class for `iwhen` statement."""

    match_re = re.compile(rf"(iwhen)(?: +{EXP_VAR})+\:$")
    value_re = re.compile(rf"iwhen((?: +{EXP_VAR})+)")
    re_flag = re.RegexFlag.IGNORECASE

    execute = enter_on_find(MultiExpStatement.execute)
