"""Module defining processor class."""

import logging

from ..tokens.statements.import_ import Import

from ..tokens.statements.define import Define

from ..compiler.compiler import Syntax
from ..reader.reader import Reader
from ..tokens.datatypes import Data
from ..tokens.functions import grammar_call, out
from ..tokens.token import Token
from ..writer.writer import Writer
from . import PAction
from .context import Context
from .grammar import Grammar, TokenList
from .triggers import Timing, Trigger

logger = logging.getLogger(__name__)


class Processor:
    """Class processing tokens."""

    def __init__(self, context: Context, syntax: Syntax) -> None:
        """Class processing the syntax."""
        self.context = context
        self._init_syntax(syntax)

    def _init_syntax(self, syntax: Syntax) -> None:
        """Set declared variables and grammar in context.

        :param syntax: Syntax to read from.
        """

        def declare_grammar(grammar: Grammar) -> None:
            """Save a grammar to the context.

            :param grammar: Grammar to save.
            :raises SyntaxError: If grammar already exists.
            """
            exists = self.context.grammars.get(grammar.name)
            if exists is None:
                self.context.grammars[grammar.name] = grammar
                return
            msg = f"Duplicate grammar in line {grammar.lineno}."
            detail = f'Grammar "{grammar.name}" already exists in line {grammar.lineno}'
            raise SyntaxError(f"{msg}\n{detail}")

        def set_var(name: str, value: Data) -> None:
            """Set a variable with a value in the context.

            :param name: Name of the variable.
            :param value: Value as a DataType object.
            """
            self.context.variables[name] = value

        for obj in syntax:
            match obj:
                case Define():
                    set_var(obj.values[0].value, obj.values[1])
                case Import():
                    raise NotImplementedError
                case Grammar():
                    declare_grammar(obj)

    @property
    def reader(self) -> Reader:
        """Alias for the contexts reader."""
        return self.context.reader

    @property
    def writer(self) -> Writer:
        """Alias for the contexts writer."""
        return self.context.writer

    def convert(self) -> Writer:
        """Transform the content according to the syntax.

        :returns: The writer object with the transformed data.
        :raises RuntimeError: If no match was found.
        """
        self.execute_grammar("input")
        if self.reader.eof:
            return self.writer
        pos = self.reader.current_pos
        unmatched = repr(self.reader.content[pos : pos + 50])
        msg = f"No match found for {unmatched}..."
        raise RuntimeError(
            f"Unmatched text in line {self.reader.current_line_number}.\n{msg}"
        )

    def execute_grammar(self, name: str) -> PAction:
        """Execute a grammars own and inherited statements.

        :param name: Name of the grammar.
        :returns: ProcessingAction of the executed syntax.
        """
        action = PAction.RESTART
        grammar = self.context.get_grammar(name)
        logger.debug("-> Executing %s", grammar)
        matched = False
        while action == PAction.RESTART:
            if grammar.inherits:
                self.execute_grammar(grammar.inherits)
            action = self.execute_tokens(grammar.tokens)
            if action == PAction.RESTART:
                matched = True
        logger.debug("<- Leaving grammar %s", name)
        if matched:
            return PAction.RESTART
        return action

    def execute_tokens(self, syntax: TokenList) -> PAction:
        """Execute a given syntax.

        :param syntax: List of Tokens to execute.
        :returns: ProcessingAction of the last executed token.
        """

        def execute_token(token: Token) -> PAction:
            """Execute a token.

            :param token: Token to execute.
            :returns: ProcessingAction of the executed token.
            """
            self.trigger(Timing.BEFORE)
            action = token.execute(self.context)
            if isinstance(token, out.Add):
                self.trigger(Timing.ON_ADD)
            self.trigger(Timing.AFTER)
            return action

        action = PAction.CONTINUE
        entered = 0
        for token in syntax:
            logger.debug("Executing %s", token)
            if isinstance(token, tuple):
                action = self.execute_condition(token)
            elif isinstance(token, grammar_call.GrammarCall):
                action = self.execute_grammar(token.name)
                if action == PAction.EXIT:
                    # continue current grammar, if called grammar is exited
                    action = PAction.CONTINUE
            else:
                if isinstance(token, (out.Open, out.Enter)):
                    entered += 1
                action = execute_token(token)
            if not action == PAction.CONTINUE:
                break
        for _ in range(entered):
            self.writer.leave_path()
        return action

    def execute_condition(self, token: tuple[Token, TokenList]) -> PAction:
        """Execute a condition.

        :param token: Tuple with condition and tokens to execute.
        :returns: ProcessingAction of the executed condition.
        """
        condition, sub_tokens = token
        action = condition.execute(self.context)
        if not action == PAction.RESTART:
            return action
        sub_action = self.execute_tokens(sub_tokens)
        if sub_action == PAction.EXIT:
            return sub_action
        return action

    def trigger(self, timing: Timing) -> None:
        """Test triggers of a timing.

        :param timing: The timing to trigger.
        """
        untriggered: list[Trigger] = []
        for trigger in self.context.queue.get(timing, []):
            if not self.reader.match(trigger.match):
                untriggered.append(trigger)
                continue
            trigger.token.execute(self)
        self.context.queue[timing] = untriggered
