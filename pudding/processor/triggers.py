"""Module defining Trigger and TriggerQueue class."""

from enum import Enum
from re import Pattern
from typing import TypeVar

from ..compiler.tokens.token import Token

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


class TriggerQueue:
    """Queue for triggers.

    :var triggers: Dictionary where the key is a timing and
        the value a list of triggers.
    """

    triggers: dict[Timing, list[Trigger]] = {}

    def __getitem__(self, key: Timing) -> list[Trigger]:
        """Get triggers with the given timing.

        :param key: Timing of the triggers.
        """
        return self.triggers[key]

    def __setitem__(self, key: Timing, value: list[Trigger]) -> None:
        """Enqueue a list of triggers at a given timing.

        :param timing: Timing of the triggers.
        :param value: Triggers to set.
        """
        self.triggers[key] = value

    def add_trigger(self, timing: Timing, trigger: Trigger) -> None:
        """Add a trigger to the queue.

        :param timing: Timing of the queue.
        :param trigger: Trigger to add.
        """
        triggers = self.triggers.get(timing, [])
        triggers.append(trigger)
        self.triggers[timing] = triggers

    def clear_triggers(self, timing: Timing | None = None) -> None:
        """Clear a trigger queue.

        :param timing: Timing of a queue to clear or none to clear all.
        """
        if timing:
            self.triggers.pop(timing)
        else:
            self.triggers = {}

    def get(self, timing: Timing, default: _D = None) -> list[Trigger] | _D:
        """Return list of triggers for a timing.

        :param timing: Timing of the triggers.
        :param default: Default value if timing is not set.
        """
        return self.triggers.get(timing, default)
