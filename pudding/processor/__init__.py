"""Processor package."""

from enum import Enum


class PAction(Enum):
    """Processing action."""

    CONTINUE = 0
    EXIT = 1
    RESTART = 2
