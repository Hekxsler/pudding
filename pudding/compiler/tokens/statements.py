"""Module defining statements."""

import re
from typing import Self, TypeVar

from ..datatypes import Data, Or, String, Varname

from ...processor import PAction
from ...processor.context import Context
from .token import Token
from ..util import EXP_VAR


_T = TypeVar("_T", bound=tuple[Data, ...])

#########################
#      Base classes     #
#########################


class Statement(Token):
    """Base class for a statement."""

    @classmethod
    def from_string(cls, string: str, lineno: int) -> Self:
        """Create Statement object from string.

        :param string: String containing the statement.
        """
        statement = cls.match_re.search(string)
        if statement is None:
            raise ValueError("Statement not in given string.")
        name = statement.group(1)
        values = cls.value_re.search(statement.group(0))
        if values is None:
            raise ValueError("No values in statement.")
        return cls(lineno, name, values.groups())

    def execute(self, context: Context) -> PAction:
        """Function for context changing actions."""
        raise NotImplementedError()


class MultiExpStatement(Statement):
    """Base class for a statement with multiple expressions."""

    value_types = (Data,)

    def _check_value_types(self, values: _T) -> _T:
        """Check type of all values."""
        for value in values:
            if isinstance(value, self.value_types[0]):
                continue
            raise TypeError(
                f"Invalid argument for {self.name} statement in line {self.lineno}"
            )
        return values

    @classmethod
    def from_string(cls, string: str, lineno: int) -> Self:
        """Parse a string into a MultiExpStatement object."""
        statement = cls.match_re.search(string)
        if not statement:
            raise ValueError("Statement not in given string.")
        name = statement.group(1)
        value_string = cls.value_re.search(statement.group(0))
        if value_string is None:
            raise ValueError("No values in statement.")
        values = re.findall(rf"{EXP_VAR}", value_string.group(1))
        return cls(lineno, name, tuple(values))

    def get_patterns(self, context: Context) -> list[str]:
        """Returns the combined patterns as a string."""
        patterns = [r""]
        for value in self.values:
            if isinstance(value, Or):
                patterns.append(r"")
                continue
            if isinstance(value, Varname):
                value = context.get_var(value.value)
            patterns[-1] += rf"({value.value})"
        return patterns

    def execute(self, context: Context) -> PAction:
        """Function for context changing actions."""
        raise NotImplementedError()


#########################
#   Statement classes   #
#########################


class Import(Statement):
    """Class for `import` statement."""

    match_re = re.compile(rf"(import) {String.regex}$")
    value_re = re.compile(rf"import ({String.regex})")
    value_types = (String,)

    def execute(self, context: Context) -> PAction:
        """Action for import statement."""
        raise SyntaxError(
            f"Import statement not defined at top level in line {self.lineno}"
        )


class Define(Statement):
    """Class for `define` statement."""

    match_re = re.compile(rf"(define) {Varname.regex} *{EXP_VAR}$")
    value_re = re.compile(rf"define ({Varname.regex}) *({EXP_VAR})")
    value_types = (Varname, Data)

    def execute(self, context: Context) -> PAction:
        """Action for define statement."""
        raise SyntaxError(
            f"Define statement not defined at top level in line {self.lineno}"
        )


class Grammar(Statement):
    """Class for `grammar` statement."""

    match_re = re.compile(r"(grammar) \w+(?:\(\w+\))?\:$")
    value_re = re.compile(r"grammar (\w+)(?:\((\w+)\))?")
    value_types = (Varname, Varname)

    def execute(self, context: Context) -> PAction:
        """Action for grammar statement."""
        raise SyntaxError(f"Grammar not defined at top level in line {self.lineno}")


class IMatch(MultiExpStatement):
    """Class for `imatch` statement."""

    match_re = re.compile(rf"(imatch)(?: {EXP_VAR})+\:$")
    value_re = re.compile(rf"imatch((?: {EXP_VAR})+)")

    def execute(self, context: Context) -> PAction:
        """Action for imatch statement."""
        for pattern in self.get_patterns(context):
            regex = re.compile(pattern, re.IGNORECASE)
            if context.reader.match(regex):
                return PAction.RESTART
        return PAction.CONTINUE


class Match(MultiExpStatement):
    """Class for `match` statement."""

    match_re = re.compile(rf"(match)(?: {EXP_VAR})+\:$")
    value_re = re.compile(rf"match((?: {EXP_VAR})+)")

    def execute(self, context: Context) -> PAction:
        """Action for match statement."""
        for pattern in self.get_patterns(context):
            regex = re.compile(pattern)
            if context.reader.match(regex):
                return PAction.RESTART
        return PAction.CONTINUE


class Skip(Match):
    """Class for `skip` statement."""

    match_re = re.compile(rf"(skip)(?: {EXP_VAR})+$")
    value_re = re.compile(rf"skip((?: {EXP_VAR})+)")


class When(MultiExpStatement):
    """Class for `when` statement."""

    match_re = re.compile(rf"(when)(?: {EXP_VAR})+\:$")
    value_re = re.compile(rf"when((?: {EXP_VAR})+)")

    def execute(self, context: Context) -> PAction:
        """Action for when statement."""
        for pattern in self.get_patterns(context):
            regex = re.compile(pattern)
            if context.reader.find(regex):
                return PAction.RESTART
        return PAction.CONTINUE


class IWhen(MultiExpStatement):
    """Class for `iwhen` statement."""

    match_re = re.compile(rf"(iwhen)(?: {EXP_VAR})+\:$")
    value_re = re.compile(rf"iwhen((?: {EXP_VAR})+)")

    def execute(self, context: Context) -> PAction:
        """Action for when statement."""
        for pattern in self.get_patterns(context):
            regex = re.compile(pattern, re.IGNORECASE)
            if context.reader.find(regex):
                return PAction.RESTART
        return PAction.CONTINUE


STATEMENTS: list[type[Statement]] = [
    Import,
    Define,
    Grammar,
    IMatch,
    Match,
    Skip,
    IWhen,
    When,
]
