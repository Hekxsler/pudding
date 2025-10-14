"""Processor package."""

from enum import Enum


class PAction(Enum):
    """Processing action."""

    CONTINUE = 0
    ENTER = 1
    EXIT = 2
    NEXT = 3
    RESTART = 4
