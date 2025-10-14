"""Module defining Reader class."""

import logging

from re import Match, Pattern

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
        """Match a regex to the content ahead and set the result as last_match.

        The attribute last_match will be set to the match object or None if it did not
        match the content ahead. If end of file has been reached, always return None.

        :param regex: The pattern to match.
        :returns: The match object or None.
        """
        logger.debug(
            "Trying to match /%s/ on %s...",
            regex.pattern,
            repr(self.content[self.current_pos : self.current_pos + 35]),
        )
        if self.eof:
            return None
        self.last_match = regex.match(self.content, self.current_pos)
        return self.last_match

    def find(self, regex: Pattern[str]) -> Match[str] | None:
        """Try matching a regex in the content ahead.

        :param regex: The pattern to match.
        :returns: The match object or None if it did not match.
        """
        return self._match(regex)

    def match(self, regex: Pattern[str]) -> Match[str] | None:
        """Try matching a regex to the content ahead and advance.
        
        If the pattern matches the current_pos is advanced by the length of the match.

        :param regex: The pattern to match.
        :returns: The match object or None if it did not match.
        """
        match = self._match(regex)
        if match is not None:
            self.current_pos += len(match.group(0))
        return match

    def would_match(self, regex: Pattern[str]) -> bool:
        """Test if a pattern would match.

        Test if a pattern would match the content ahead without advancing the current
        position or changing the last_match attribute of the reader.

        :param trigger: The trigger object.
        :returns: Boolean if trigger matches.
        """
        return regex.match(self.content, self.current_pos) is not None
