"""Base control function class."""

from typing import NoReturn

from ....processor import PAction
from ....processor.context import Context
from ..function import Function


class Do(Function):
    """Base class for control functions."""

    value_types = tuple()

    def execute(self, context: Context) -> PAction | NoReturn:
        """Action for control functions."""
        raise NotImplementedError()
