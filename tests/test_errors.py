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


def test_define() -> None:
    """Test define statement."""
    with pytest.raises(TypeError, match="type"):
        convert_string("define 'a' | 'b'\n\ngrammar input:\n    fail", "", "xml")
    with pytest.raises(SyntaxError, match="can not contain"):
        convert_string("define test 'a' | 'b'\n\ngrammar input:\n    fail", "", "xml")


def test_function() -> None:
    """Test function."""
    with pytest.raises(SyntaxError, match="Missing"):
        convert_string("grammar input:\n    out.open()", "", "xml")
    with pytest.raises(SyntaxError, match="too many"):
        convert_string("grammar input:\n    out.open('a','b','c')", "", "xml")


def test_import() -> None:
    """Test import statement."""
    with pytest.raises(SyntaxError, match="import"):
        convert_string("grammar input:\n    import 'a'", "", "xml")
    with pytest.raises(SyntaxError, match="import"):
        convert_string("grammar input:\n    from 'a' import 'B'", "", "xml")


def test_fail() -> None:
    """Test fail statement."""
    with pytest.raises(RuntimeError, match="Fail statement"):
        convert_string("grammar input:\n    fail", "", "xml")
    with pytest.raises(RuntimeError, match=r"testXmessage"):
        convert_string("grammar input:\n    fail 'testXmessage'", "", "xml")
