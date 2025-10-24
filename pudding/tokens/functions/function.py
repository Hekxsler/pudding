"""Module defining functions."""

from typing import NoReturn, TypeVar

from ...datatypes import Data, String
from ...processor import PAction
from ...processor.context import Context
from ..token import Token

OPTIONAL_STRING = rf"(?:\, *({String.regex}))?"
_D = TypeVar("_D")


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
        err_msg = f"Expected {self.min_args} but got {len(values)}"
        if len(values) < self.min_args:
            raise SyntaxError(f"Missing arguments in line {lineno}. {err_msg}")
        if len(values) > self.max_args:
            raise SyntaxError(f"Too many arguments in line {lineno}. {err_msg}")
        super().__init__(lineno, name, values)

    def execute(self, context: Context) -> PAction | NoReturn:
        """Execute this token.

        :param context: Current context object.
        :returns: Returns PAction for processor class.
        """
        raise NotImplementedError()

    def get_string(self, index: int) -> String:
        """Get String object in values.

        :param index: Index of the object in values.
        :returns: The String object at the given index.
        :raises TypeError: If object at given index is not of type String.
        """
        value = self.values[index]
        if isinstance(value, String):
            return value
        raise TypeError(f"Value {repr(value)} is not a string. (line {self.lineno})")
