"""Test module for pudding.util."""

from pathlib import Path
from pudding import convert_file


def _same_file(file_1: str, file_2: str) -> bool:
    """Compare two files and check if they have the same content."""
    content_1 = open(file_1, "r", encoding="utf-8").read()
    content_2 = open(file_2, "r", encoding="utf-8").read()
    return content_1 == content_2


def test_convert_file_json() -> None:
    """Test convert_file function for JSON output."""
    data_dir = Path(__file__).parent / "data"
    pud_file = data_dir / "test.pud"
    input_file = data_dir / "input.txt"
    convert_file(pud_file, input_file, data_dir / "result.json", "json")
    assert _same_file(str(data_dir / "result.json"), str(data_dir / "expected.json"))


def test_convert_file_xml() -> None:
    """Test convert_file function for XML output."""
    data_dir = Path(__file__).parent / "data"
    pud_file = data_dir / "test.pud"
    input_file = data_dir / "input.txt"
    convert_file(pud_file, input_file, data_dir / "result.xml", "xml")
    assert _same_file(str(data_dir / "result.xml"), str(data_dir / "expected.xml"))


def test_convert_file_yaml() -> None:
    """Test convert_file function for YAML output."""
    data_dir = Path(__file__).parent / "data"
    pud_file = data_dir / "test.pud"
    input_file = data_dir / "input.txt"
    convert_file(pud_file, input_file, data_dir / "result.yaml", "yaml")
    assert _same_file(str(data_dir / "result.yaml"), str(data_dir / "expected.yaml"))
