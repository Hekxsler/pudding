"""Module defining context class."""

from ..tokens.datatypes import Data, Varname
from ..reader.reader import Reader
from ..writer.writer import Writer
from .grammar import Grammar
from .triggers import TriggerQueue


class Context:
    """Class containing context for the processor.

    :var grammars: Grammars defined in the syntax.
    :var queue: Queue for triggers created by enqueued statements.
    :var variables: Variables defined in the syntax.
    """

    def __init__(self, content: str, writer_cls: type[Writer]) -> None:
        """Init for Context class.

        :param content: Content of the file to convert.
        :param writer_cls: Writer class for generating output.
        """
        self.grammars: dict[str, Grammar] = {}
        self.queue: TriggerQueue = TriggerQueue()
        self.variables: dict[str, Data] = {}
        self.reader = Reader(content)
        self.writer = writer_cls()

    def get_grammar(self, name: str) -> Grammar:
        """Get a grammar by name.

        :param name: Name of the grammar to retrieve.
        :raises SyntaxError: If grammar is not defined.
        """
        grammar = self.grammars.get(name)
        if not grammar:
            raise SyntaxError(f'Grammar "{name}" is not defined.')
        return grammar

    def get_var(self, name: str) -> Data:
        """Get a variable by name.

        :param name: Name of the variable to retrieve.
        :raises NameError: If variable is not defined.
        """
        value = self.variables.get(name)
        if not value:
            raise NameError(f'Variable "{name}" is not defined.')
        if isinstance(value, Varname):
            value = self.get_var(value.value)
        return value
