"""Test module for cli functions."""

import json

from pudding._cli import main

from .test_util import DATA_DIR, INPUT_FILE


def test_main() -> None:
    """Test main function."""
    pud_file = DATA_DIR / "test.pud"
    main(["-s", str(pud_file), str(INPUT_FILE), "-f", "json"])
    assert json.load(open(DATA_DIR / "input.json")) == json.load(
        open(DATA_DIR / "expected.json")
    )
