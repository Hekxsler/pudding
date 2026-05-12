"""Output function out.enqueue_after."""

import re

from pudding.datatypes import Regex, String, Varname
from pudding.processor import PAction
from pudding.processor.context import Context
from pudding.processor.triggers import Timing, Trigger

from ..function import Function
from .add import Add


class Enqueue(Function):
    """Base class for `out.enqueue` functions."""

    min_args = 2
    max_args = 3
    value_types = (String | Regex | Varname, String, String)

    def get_pattern(self, context: Context) -> re.Pattern[str]:
        """Return pattern to match."""
        value = self.values[0].re_pattern
        if isinstance(self.values[0], Varname):
            value = context.get_var(self.values[0])
        return re.compile(value)

    def get_values(self) -> tuple[String, ...]:
        """Get values to create tag."""
        if not self.get_value(2):
            return (self.get_string(1),)
        return (self.get_string(1), self.get_string(2))

    def add_trigger(self, context: Context, timing: Timing) -> PAction:
        """Add trigger to context."""
        context.queue.add_trigger(
            timing,
            Trigger(
                self.get_pattern(context),
                Add(self.lineno, "EnqueuedAdd", self.get_values()),
            ),
        )
        return PAction.CONTINUE


class EnqueueAfter(Enqueue):
    """Class for `out.enqueue_after` function.

    Like out.add(), but is executed after the given regular expression
    matches the input and the next token was processed.
    """

    match_re = re.compile(r"(out\.enqueue_after)\((.*)\)$")

    def execute(self, context: Context) -> PAction:
        """Enqueue token after execution.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        self.add_trigger(context, Timing.AFTER)
        return PAction.CONTINUE


class EnqueueBefore(Enqueue):
    """Class for `out.enqueue_before` function.

    Like out.add(), but is executed as soon as the given regular expression
    matches the input, regardless of the grammar in which the match occurs.
    """

    match_re = re.compile(r"(out\.enqueue_before)\((.*)\)$")

    def execute(self, context: Context) -> PAction:
        """Enqueue token before execution.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        self.add_trigger(context, Timing.BEFORE)
        return PAction.CONTINUE


class EnqueueOnAdd(Enqueue):
    """Class for `out.enqueue_on_add` function.

    Like out.add(), but is executed after the given regular expression
    matches the input and the next node is added to the output.
    """

    match_re = re.compile(r"(out\.enqueue_on_add)\((.*)\)$")

    def execute(self, context: Context) -> PAction:
        """Enqueue token on execution of out.add().

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        self.add_trigger(context, Timing.ON_ADD)
        return PAction.CONTINUE
