"""Base output function class."""

from ....processor import PAction
from ....processor.context import Context
from ..function import Function


class Out(Function):
    """Base class for output generation functions."""

    min_args = 1
    max_args = 2

    def execute(self, context: Context) -> PAction:
        """Execute this token.

        :param context: Current context object.
        :raises NotImplementedError: Abstract method
        """
        raise NotImplementedError()
