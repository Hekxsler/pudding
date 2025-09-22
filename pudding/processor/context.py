"""Module defining context class"""

from ..compiler.datatypes import Data, Varname
from .grammar import Grammar
from ..reader.reader import Reader
from ..writer.writer import Writer
from .triggers import Timing, Trigger, TriggerQueue


class Context:
    """Class giving context to current match."""

    grammars: dict[str, Grammar] = {}
    queue: TriggerQueue = TriggerQueue()
    variables: dict[str, Data] = {}

    def __init__(self, content: str, writer_cls: type[Writer]) -> None:
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

    def trigger(self, timing: Timing) -> None:
        """Trigger a timing."""
        untriggered: list[Trigger] = []
        for trigger in self.queue.get(timing, []):
            if not self.reader.match(trigger.match):
                untriggered.append(trigger)
                continue
            trigger.token.execute(self)
        self.queue[timing] = untriggered
