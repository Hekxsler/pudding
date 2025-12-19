"""Test module for pudding.util."""

import json
import yaml

from lxml import etree
from pathlib import Path
from pudding import convert_file

DATA_DIR = Path(__file__).parent / "data"
INPUT_FILE = DATA_DIR / "input.txt"


def test_convert_file_json() -> None:
    """Test convert_file function for JSON output."""
    pud_file = DATA_DIR / "test.pud"
    convert_file(pud_file, INPUT_FILE, DATA_DIR / "result.json", "json")
    assert json.load(open(DATA_DIR / "result.json")) == json.load(
        open(DATA_DIR / "expected.json")
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
    pud_file = DATA_DIR / "test.pud"
    convert_file(pud_file, INPUT_FILE, DATA_DIR / "result.xml", "xml")
    tree1 = etree.parse(open(DATA_DIR / "result.xml"))
    tree2 = etree.parse(open(DATA_DIR / "expected.xml"))
    assert elements_equal(tree1.getroot(), tree2.getroot())


def test_convert_file_slixml() -> None:
    """Test convert_file function for SliXML output."""
    pud_file = DATA_DIR / "slixml.pud"
    convert_file(pud_file, INPUT_FILE, DATA_DIR / "result.slixml", "slixml")
    tree1 = etree.parse(open(DATA_DIR / "result.slixml", encoding="utf-8"))
    tree2 = etree.parse(open(DATA_DIR / "expected.slixml"))
    assert elements_equal(tree1.getroot(), tree2.getroot())


def test_convert_file_yaml() -> None:
    """Test convert_file function for YAML output."""
    pud_file = DATA_DIR / "test.pud"
    convert_file(pud_file, INPUT_FILE, DATA_DIR / "result.yaml", "yaml")
    assert yaml.safe_load(open(DATA_DIR / "result.yaml")) == yaml.safe_load(
        open(DATA_DIR / "expected.yaml")
    )
