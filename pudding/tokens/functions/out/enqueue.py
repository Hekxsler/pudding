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


class EnqueueAfter(Out):
    """Class for `out.enqueue_after` function.

    Like out.add(), but is executed after the given regular expression
    matches the input and the next match statement was processed.
    """

    min_args = 2
    max_args = 3

    match_re = re.compile(
        rf"(out\.enqueue_after)\({EXP_VAR}, *{String.regex}{OPTIONAL_STRING}\)$"
    )
    value_re = re.compile(
        rf"out\.enqueue_after\(({EXP_VAR}), *({String.regex}){OPTIONAL_STRING}\)"
    )
    value_types = (Regex | Varname, String, String)

    def execute(self, context: Context) -> PAction:
        """Action for enqueue_after function."""
        values = [self.get_replaced_string(1, context)]
        if isinstance(self.get_value(2), String):
            values.append(self.get_replaced_string(2, context))
        context.queue.add_trigger(
            Timing.AFTER,
            Trigger(
                re.compile(self.values[0].value),
                Add(self.lineno, "EnqueuedAdd", tuple(values)),
            ),
        )
        return PAction.CONTINUE


class EnqueueBefore(Out):
    """Class for `out.enqueue_before` function.

    Like out.add(), but is executed as soon as the given regular expression
    matches the input, regardless of the grammar in which the match occurs.
    """

    min_args = 2
    max_args = 3

    match_re = re.compile(
        rf"(out\.enqueue_before)\({EXP_VAR}, *{String.regex}{OPTIONAL_STRING}\)$"
    )
    value_re = re.compile(
        rf"out\.enqueue_before\(({EXP_VAR}), *({String.regex}){OPTIONAL_STRING}\)"
    )
    value_types = (Regex | Varname, String, String)

    def execute(self, context: Context) -> PAction:
        """Action for enqueue_before function."""
        values = [self.get_replaced_string(1, context)]
        if isinstance(self.get_value(2), String):
            values.append(self.get_replaced_string(2, context))
        context.queue.add_trigger(
            Timing.BEFORE,
            Trigger(
                re.compile(self.values[0].value),
                Add(self.lineno, "EnqueuedAdd", tuple(values)),
            ),
        )
        return PAction.CONTINUE


class EnqueueOnAdd(Out):
    """Class for `out.enqueue_on_add` function.

    Like out.add(), but is executed after the given regular expression
    matches the input and the next node is added to the output.
    """

    min_args = 2
    max_args = 3

    match_re = re.compile(
        rf"(out\.enqueue_on_add)\({EXP_VAR}, *{String.regex}{OPTIONAL_STRING}\)$"
    )
    value_re = re.compile(
        rf"out\.enqueue_on_add\(({EXP_VAR}), *({String.regex}){OPTIONAL_STRING}\)"
    )
    value_types = (Regex | Varname, String, String)

    def execute(self, context: Context) -> PAction:
        """Action for enqueue_on_add function."""
        values = [self.get_replaced_string(1, context)]
        if isinstance(self.get_value(2), String):
            values.append(self.get_replaced_string(2, context))
        context.queue.add_trigger(
            Timing.ON_ADD,
            Trigger(
                re.compile(self.values[0].value),
                Add(self.lineno, "EnqueuedAdd", tuple(values)),
            ),
        )
        return PAction.CONTINUE
