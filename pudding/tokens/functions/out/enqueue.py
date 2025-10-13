"""Output function out.enqueue_after."""

import re

from ....processor import PAction
from ....processor.context import Context
from ....processor.triggers import Timing, Trigger
from ...datatypes import Regex, String, Varname
from ...util import EXP_VAR
from ..function import OPTIONAL_STRING
from .add import Add
from .out import Out


class Enqueue(Out):
    """Base class for `out.enqueue` functions."""

    min_args = 2
    max_args = 3
    value_types = (String | Regex | Varname, String, String)

    def add_trigger(self, context: Context, timing: Timing) -> PAction:
        """Add trigger to context."""
        if isinstance(self, Varname):
            pattern = context.get_var(self.values[0].value)
        else:
            pattern = self.values[0].pattern
        values = [self.values[1]]
        if isinstance(self.get_value(2), String):
            values.append(self.values[2])
        context.queue.add_trigger(
            timing,
            Trigger(
                pattern,
                Add(self.lineno, "EnqueuedAdd", tuple(values)),
            ),
        )
        return PAction.CONTINUE


class EnqueueAfter(Enqueue):
    """Class for `out.enqueue_after` function.

    Like out.add(), but is executed after the given regular expression
    matches the input and the next match statement was processed.
    """

    match_re = re.compile(
        rf"(out\.enqueue_after)\({EXP_VAR}, *{String.regex}{OPTIONAL_STRING}\)$"
    )
    value_re = re.compile(
        rf"out\.enqueue_after\(({EXP_VAR}), *({String.regex}){OPTIONAL_STRING}\)"
    )

    def execute(self, context: Context) -> PAction:
        """Action for enqueue_after function."""
        self.add_trigger(context, Timing.AFTER)
        return PAction.CONTINUE


class EnqueueBefore(Enqueue):
    """Class for `out.enqueue_before` function.

    Like out.add(), but is executed as soon as the given regular expression
    matches the input, regardless of the grammar in which the match occurs.
    """

    match_re = re.compile(
        rf"(out\.enqueue_before)\({EXP_VAR}, *{String.regex}{OPTIONAL_STRING}\)$"
    )
    value_re = re.compile(
        rf"out\.enqueue_before\(({EXP_VAR}), *({String.regex}){OPTIONAL_STRING}\)"
    )

    def execute(self, context: Context) -> PAction:
        """Action for enqueue_before function."""
        self.add_trigger(context, Timing.BEFORE)
        return PAction.CONTINUE


class EnqueueOnAdd(Enqueue):
    """Class for `out.enqueue_on_add` function.

    Like out.add(), but is executed after the given regular expression
    matches the input and the next node is added to the output.
    """

    match_re = re.compile(
        rf"(out\.enqueue_on_add)\({EXP_VAR}, *{String.regex}{OPTIONAL_STRING}\)$"
    )
    value_re = re.compile(
        rf"out\.enqueue_on_add\(({EXP_VAR}), *({String.regex}){OPTIONAL_STRING}\)"
    )

    def execute(self, context: Context) -> PAction:
        """Action for enqueue_on_add function."""
        self.add_trigger(context, Timing.ON_ADD)
        return PAction.CONTINUE
