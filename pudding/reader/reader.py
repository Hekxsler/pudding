"""Module defining Reader class."""

import logging

from re import Match, Pattern

from ..processor.triggers import Trigger

logger = logging.getLogger(__name__)


class Reader:
    """Base Reader class.

    :var current_pos: Current position in content.
    :var last_match: Last Match object or None if regex did not match.
    """

    current_pos = 0
    last_match: Match[str] | None = None

    def __init__(self, content: str) -> None:
        """Init class."""
        self.content = content
        self.endpos = len(content)

    @property
    def eof(self) -> bool:
        """Boolean if end of content has been reached."""
        return self.current_pos >= self.endpos

    @property
    def current_line_number(self) -> int:
        """Line number of the current position."""
        return self.content.count("\n", None, self.current_pos) + 1

    def _match(self, regex: Pattern[str]) -> Match[str] | None:
        """Try matching a regex to the content ahead and set the result as last_match.

        :param regex: The pattern to match.
        :returns: The match or None if it did not match.
        """
        logger.debug("Trying to match /%s/", regex.pattern)
        if self.eof:
            return None
        self.last_match = regex.match(self.content, self.current_pos)
        return self.last_match

    def find(self, regex: Pattern[str]) -> Match[str] | None:
        """Try finding a match for the regex in the content ahead."""
        return self._match(regex)

    def match(self, regex: Pattern[str]) -> Match[str] | None:
        """Try matching a regex to the content ahead and advance."""
        match = self._match(regex)
        if match is not None:
            self.current_pos += len(match.group(0))
        return match

    def test_trigger(self, trigger: Trigger) -> bool:
        """Test if a trigger matches.

        :param trigger: The trigger object.
        :returns: Boolean if trigger matches.
        """
        return trigger.match.match(self.content, self.current_pos) is not None
