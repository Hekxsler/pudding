"""Output function out.clear_triggers."""

import re

from pudding.processor import PAction
from pudding.processor.context import Context

from ..function import Function


class ClearQueue(Function):
    """Class for `out.clear_queue` function.

    Removes any items from the queue that were previously queued
    using the out.enqueue_*() functions.
    """

    min_args = 0
    max_args = 0

    match_re = re.compile(r"(out\.clear_queue)\((.*)\)$")
    value_types = tuple()

    def execute(self, context: Context) -> PAction:
        """Clear enqueued tokens.

        :param context: Current context object.
        :returns: PAction.CONTINUE
        """
        context.queue.clear_triggers()
        return PAction.CONTINUE
