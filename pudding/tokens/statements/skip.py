"""Skip statement."""

import re
from typing import Callable

from pudding.processor import PAction
from pudding.processor.context import Context

from ..util import EXP_VAR
from .match import IMatch, Match


def skip_on_match(method: Callable[..., PAction]) -> Callable[..., PAction]:
    def wrapper(self: "Skip | ISkip", context: Context) -> PAction:
        action = method(self, context)
        if action == PAction.ENTER:
            return PAction.RESTART
        return PAction.NEXT

    return wrapper


class Skip(Match):
    """Class for `skip` statement."""

    match_re = re.compile(rf"(skip)(?: +{EXP_VAR})+$")
    value_re = re.compile(rf"skip((?: +{EXP_VAR})+)")

    execute = skip_on_match(Match.execute)


class ISkip(IMatch):
    """Class for `iskip` statement."""

    match_re = re.compile(rf"(iskip)(?: +{EXP_VAR})+$")
    value_re = re.compile(rf"iskip((?: +{EXP_VAR})+)")

    execute = skip_on_match(IMatch.execute)
