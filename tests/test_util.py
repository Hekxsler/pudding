"""Test module for pudding.util."""

import json
import yaml

from lxml import etree
from pathlib import Path
from pudding import convert_file


def test_convert_file_json() -> None:
    """Test convert_file function for JSON output."""
    data_dir = Path(__file__).parent / "data"
    pud_file = data_dir / "test.pud"
    input_file = data_dir / "input.txt"
    convert_file(pud_file, input_file, data_dir / "result.json", "json")
    assert json.load(open(data_dir / "result.json")) == json.load(
        open(data_dir / "expected.json")
    )


def elements_equal(elem1: etree.Element, elem2: etree.Element) -> bool:
    """Compare two lxml.Element objects."""
    if (
        elem1.tag != elem2.tag
        or elem1.text != elem2.text
        or elem1.attrib != elem2.attrib
    ):
        return False
    if len(elem1) != len(elem2):
        return False
    return all(elements_equal(c1, c2) for c1, c2 in zip(elem1, elem2))


def test_convert_file_xml() -> None:
    """Test convert_file function for XML output."""
    data_dir = Path(__file__).parent / "data"
    pud_file = data_dir / "test.pud"
    input_file = data_dir / "input.txt"
    convert_file(pud_file, input_file, data_dir / "result.xml", "xml")
    tree1 = etree.parse(open(data_dir / "result.xml"))
    tree2 = etree.parse(open(data_dir / "expected.xml"))
    assert elements_equal(tree1.getroot(), tree2.getroot())


def test_convert_file_yaml() -> None:
    """Test convert_file function for YAML output."""
    data_dir = Path(__file__).parent / "data"
    pud_file = data_dir / "test.pud"
    input_file = data_dir / "input.txt"
    convert_file(pud_file, input_file, data_dir / "result.yaml", "yaml")
    assert yaml.safe_load(open(data_dir / "result.yaml")) == yaml.safe_load(
        open(data_dir / "expected.yaml")
    )
