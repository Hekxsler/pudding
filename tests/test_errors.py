"""Test module for exceptions."""

import pytest

from pudding.util import convert_string


def test_define() -> None:
    """Test define statement."""
    with pytest.raises(TypeError, match="type"):
        convert_string("define 'a' | 'b'\n\ngrammar input:\n    fail", "", "xml")
    with pytest.raises(SyntaxError, match=r"[Dd]efine"):
        convert_string("define test 'a' | 'b'\n\ngrammar input:\n    fail", "", "xml")


def test_function() -> None:
    """Test function."""
    with pytest.raises(SyntaxError, match=r"[Mm]issing"):
        convert_string("grammar input:\n    out.open()", "", "xml")
    with pytest.raises(SyntaxError, match=r"[Tt]oo many"):
        convert_string("grammar input:\n    out.open('a','b','c')", "", "xml")


def test_import() -> None:
    """Test import statement."""
    with pytest.raises(SyntaxError, match=r"[Ii]mport"):
        convert_string("grammar input:\n    import 'a'", "", "xml")
    with pytest.raises(SyntaxError, match=r"[Ii]mport"):
        convert_string("grammar input:\n    from 'a' import 'B'", "", "xml")


def test_fail() -> None:
    """Test fail statement."""
    with pytest.raises(RuntimeError, match=r"[Ff]ail statement"):
        convert_string("grammar input:\n    fail", "", "xml")
    with pytest.raises(RuntimeError, match=r"testXmessage"):
        convert_string("grammar input:\n    fail 'testXmessage'", "", "xml")
