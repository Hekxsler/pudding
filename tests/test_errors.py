"""Test module for exceptions."""

import pytest

from pudding.util import convert_string


SYNTAX = """
grammar input:
    out.open()
"""

CONTENT = """User
----
Name: John, Lastname: Doe
Office: 1st Ave
Birth date: 1978-01-01
"""


def test_function() -> None:
    """Test function."""
    with pytest.raises(SyntaxError):
        convert_string("grammar input:\n    out.open()", "", "xml")
    with pytest.raises(SyntaxError):
        convert_string("grammar input:\n    out.open('a','b','c')", "", "xml")


def test_fail() -> None:
    """Test fail statement."""
    with pytest.raises(RuntimeError):
        convert_string("grammar input:\n    fail", "", "xml")
    with pytest.raises(RuntimeError, match=r"testXmessage"):
        convert_string("grammar input:\n    fail 'testXmessage'", "", "xml")
