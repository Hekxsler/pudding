"""Skip statement."""

import re
from typing import Callable

from pudding.processor import PAction
from pudding.processor.context import Context

from .match import IMatch, Match


def skip_on_match(method: Callable[..., PAction]) -> Callable[..., PAction]:
    """Skip text when it matches."""

    def wrapper(self: "Skip | ISkip", context: Context) -> PAction:
        action = method(self, context)
        if action == PAction.ENTER:
            return PAction.RESTART
        return PAction.NEXT

    return wrapper


class Skip(Match):
    """Class for `skip` statement."""

    match_re = re.compile(r"(skip) (.*)$")

    execute = skip_on_match(Match.execute)


class ISkip(IMatch):
    """Class for `iskip` statement."""

    match_re = re.compile(r"(iskip) (.*)$")

    execute = skip_on_match(IMatch.execute)
