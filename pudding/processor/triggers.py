"""Module defining Trigger and TriggerQueue class."""

from enum import Enum
from re import Pattern
from typing import TypeVar

from ..tokens.token import Token

Timing = Enum("Timing", "AFTER BEFORE ON_ADD")
_D = TypeVar("_D")


class Trigger:
    """Base trigger class."""

    def __init__(self, match: Pattern[str], token: Token) -> None:
        """Trigger class.

        :param match: Pattern to match before executing.
        :param token: Token to execute on match.
        """
        self.match = match
        self.token = token

    def __repr__(self) -> str:
        """Return string representation of this object."""
        cls = self.__class__.__name__
        return f"<{cls} match=/{self.match.pattern}/ token={self.token}>"


class TriggerQueue(dict[Timing, list[Trigger]]):
    """Queue for triggers.

    :var triggers: Dictionary where the key is a timing and
        the value a list of triggers.
    """

    def add_trigger(self, timing: Timing, trigger: Trigger) -> None:
        """Add a trigger to the queue.

        :param timing: Timing of the queue.
        :param trigger: Trigger to add.
        """
        triggers = self.get(timing, [])
        triggers.append(trigger)
        self[timing] = triggers

    def clear_triggers(self, timing: Timing | None = None) -> None:
        """Clear a trigger queue.

        :param timing: Timing of a queue to clear or none to clear all.
        """
        if timing:
            del self[timing]
        else:
            self.triggers: dict[Timing, list[Trigger]] = {}
