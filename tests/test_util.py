"""Test module for pudding.util."""

from pudding import convert_file


def _same_file(file_1: str, file_2: str) -> bool:
    """Compare two files and check if they are identical."""
    content_1 = open(file_1, "r", encoding="utf-8").read()
    content_2 = open(file_2, "r", encoding="utf-8").read()
    return content_1 == content_2


def test_convert_file() -> None:
    """Test convert_file function."""
    convert_file("./data/test.pud", "./data/input.txt", "./data/result.json", "json")
    assert _same_file("./data/result.json", "./data/expected.json")
    convert_file("./data/test.pud", "./data/input.txt", "./data/result.xml", "xml")
    assert _same_file("./data/result.xml", "./data/expected.xml")
    convert_file("./data/test.pud", "./data/input.txt", "./data/result.yaml", "yaml")
    assert _same_file("./data/result.yaml", "./data/expected.yaml")
