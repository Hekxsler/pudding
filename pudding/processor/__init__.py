"""Processor package."""

from enum import Enum

PAction = Enum("ProcessingAction", names="CONTINUE EXIT RESTART")
