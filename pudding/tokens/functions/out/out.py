"""Base output function class."""

from ..function import Function


class Out(Function):
    """Base class for output generation functions."""

    min_args = 1
    max_args = 2
