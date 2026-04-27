"""Module defining functions."""

from ...datatypes import Data, String
from ..token import Token

OPTIONAL_STRING = rf"(?:\, *({String.regex}))?"


class Function(Token):
    """Base class for a function.

    :var min_args: Minimum amount of arguments.
    :var max_args: Maximum amount of arguments.
    """

    min_args = 0
    max_args = 0

    def __init__(self, lineno: int, name: str, values: tuple[Data, ...]) -> None:
        """Init for Function class.

        :param lineno: Line number in .pud file.
        :param name: Name of the function.
        :param values: Values of the arguments.
        :raises SyntaxError:
        """
        if self.min_args <= len(values) <= self.max_args:
            return super().__init__(lineno, name, values)
        err_msg = f"Expected {self.min_args} but got {len(values)}"
        if len(values) < self.min_args:
            raise SyntaxError(f"Missing arguments in line {lineno}. {err_msg}")
        raise SyntaxError(f"Too many arguments in line {lineno}. {err_msg}")
