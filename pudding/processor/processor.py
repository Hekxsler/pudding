"""Module defining processor class."""

import logging

from ..compiler.compiler import Syntax
from ..reader.reader import Reader
from ..tokens.functions import grammar_call, out
from ..tokens.statements.define import Define
from ..tokens.token import Token
from ..writer import Writer
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
            """Set a grammar in the context.

            :param grammar: Grammar to declare.
            """
            exists = self.context.grammars.get(grammar.name)
            if exists is not None:
                logger.warning(
                    "Duplicate grammar %s in line %s already exists in line %s.",
                    repr(grammar.name),
                    grammar.lineno,
                    exists.lineno,
                )
            self.context.grammars[grammar.name] = grammar

        for obj in syntax:
            match obj:
                case Define():
                    obj.execute(self.context)
                case Grammar():
                    declare_grammar(obj)
                case _:
                    raise RuntimeError(f"Unprocessed statement {obj}.")

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
        """Execute a grammar by name.

        Execute tokens of a grammar with the given name. If a inherited grammar
        exists, it will be executed first.

        :param name: Name of the grammar.
        :returns: PAction.RESTART if grammar restarted at least once
            else PAction.CONTINUE.
        """
        grammar = self.context.get_grammar(name)
        logger.debug("-> Executing %s", grammar)
        action = PAction.RESTART
        restarts: int = 0
        while action == PAction.RESTART:
            restarts += 1
            if grammar.inherits:
                self.execute_grammar(grammar.inherits)
            action = self._execute_grammar(grammar)
        logger.debug("<- Leaving grammar %s", name)
        if restarts > 1:
            return PAction.RESTART
        return PAction.CONTINUE

    def execute_condition(self, token: tuple[Token, TokenList]) -> PAction:
        """Execute a condition.

        The condition token will return PAction.ENTER if sub tokens should be
        executed. Otherwise the condition is not met and sub tokens not executed.
        If all sub tokens have been executed, restart the grammar unless another
        PAction than CONTINUE is requested.

        :param token: Tuple with condition and tokens to execute.
        :returns: ProcessingAction.
        """
        condition, sub_tokens = token
        action = condition.execute(self.context)
        if not action == PAction.ENTER:
            return action
        sub_action = self._execute_tokens(sub_tokens)
        if sub_action == PAction.CONTINUE:
            return PAction.RESTART
        return sub_action

    def execute_token(self, token: Token) -> PAction:
        """Execute a token.

        Execute the token and trigger Timings before and after the execution.

        :param token: Token to execute.
        :returns: PAction of the executed token.
        """
        self.trigger(Timing.BEFORE)
        action = token.execute(self.context)
        if isinstance(token, (out.Add, out.Create)):
            self.trigger(Timing.ON_ADD)
        self.trigger(Timing.AFTER)
        return action

    def _execute_grammar(self, grammar: Grammar) -> PAction:
        """Execute tokens of a grammar.

        Opened and entered writer paths are left at the end of the grammar.
        PAction.NEXT is treated as PAction.CONTINUE so the next token of
        the grammar is executed.

        :param syntax: Grammar to execute.
        :returns: PAction of the last executed token.
        """
        action = PAction.EXIT
        entered = 0
        for token in grammar.tokens:
            logger.debug("Executing %s", token)
            match token:
                case tuple():
                    action = self.execute_condition(token)
                case grammar_call.GrammarCall():
                    action = self.execute_grammar(token.name)
                case out.Open() | out.Enter():
                    entered += 1
                    action = self.execute_token(token)
                case _:
                    action = self.execute_token(token)
            if action not in (PAction.CONTINUE, PAction.NEXT):
                break
        self.writer.leave_paths(entered)
        return action

    def _execute_tokens(self, tokens: TokenList) -> PAction:
        """Execute a TokenList.

        Opened and entered writer paths are left at the end of the grammar.
        If a token returns not PAction.CONTINUE, stop executing and return
        the last PAction.

        :param syntax: List of Tokens to execute.
        :returns: PAction of the last executed token.
        """
        action = PAction.CONTINUE
        entered = 0
        for token in tokens:
            logger.debug("Executing %s", token)
            match token:
                case tuple():
                    action = self.execute_condition(token)
                case grammar_call.GrammarCall():
                    action = self.execute_grammar(token.name)
                case out.Open() | out.Enter():
                    entered += 1
                    action = self.execute_token(token)
                case _:
                    action = self.execute_token(token)
            if action != PAction.CONTINUE:
                break
        self.writer.leave_paths(entered)
        return action

    def trigger(self, timing: Timing) -> None:
        """Test triggers of a timing.

        :param timing: The timing to trigger.
        """
        untriggered: list[Trigger] = []
        for trigger in self.context.queue.get(timing, []):
            if not self.reader.would_match(trigger.match):
                untriggered.append(trigger)
                continue
            logger.debug("Triggered trigger %s", trigger)
            self.reader.match(trigger.match)
            trigger.token.execute(self.context)
        self.context.queue[timing] = untriggered
