"""Module defining context class."""

import re

from ..datatypes.string import String
from ..reader.reader import Reader
from ..writer.writer import Writer
from .grammar import Grammar
from .triggers import TriggerQueue

STRING_VAR_RE = r"([^\d]?\$(\d+)[^\$]?)"
# match chars before and after to not match $1 and $10 when replacing $1


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
        self.variables: dict[str, re.Pattern[str]] = {}
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

    def get_var(self, name: str) -> re.Pattern[str]:
        """Get a variable by name.

        :param name: Name of the variable to retrieve.
        :raises NameError: If variable is not defined.
        """
        value = self.variables.get(name)
        if not value:
            raise NameError(f'Variable "{name}" is not defined.')
        return value

    def replace_string_vars(self, string: String) -> str:
        """Replace variables in a string with the last matched values.

        :param string: String to replace vars in.
        :param context: The current context.
        :returns: The string with replaced values.
        """
        string_vars = re.findall(STRING_VAR_RE, string.value)
        if len(string_vars) == 0:
            return string.value
        if self.reader.last_match is None:
            raise RuntimeError(
                "Can not replace variables, because no expression matched yet."
            )
        new_string = string.value
        matches = self.reader.last_match.groups()
        for replace, i in string_vars:
            assert isinstance(replace, str)
            if int(i) >= len(matches):
                raise IndexError(f"Not enough matches in {matches} to replace variable '${i}'.")
            value = replace.replace(f"${i}", matches[int(i)])
            new_string = re.sub(re.escape(replace), value, new_string)
        return new_string
