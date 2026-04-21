"""Main script."""

import argparse
import datetime
import logging
import os
from collections.abc import Sequence
from pathlib import Path

from . import __version__
from .util import convert_files

DESCRIPTION = """
Pudding converts text to a structured format, such as XML, JSON or YAML.
For more information see the documentation at https://pudding.readthedocs.io/latest.
"""
FORMAT_CHOICES = ["json", "slixml", "xml", "yaml"]

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser."""
    parser = argparse.ArgumentParser(prog="pudding", description=DESCRIPTION)
    parser.add_argument(
        "filename", metavar="FILE", help="The file or files to convert.", nargs="+"
    )
    parser.add_argument(
        "-s",
        "--syntax",
        default=None,
        help="The file containing the syntax for parsing the input.",
        metavar="SYNTAX_FILE",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=FORMAT_CHOICES,
        default="xml",
        help=(
            "The output format. "
            f"Choices are: {', '.join(FORMAT_CHOICES)}. Default is `xml`."
        ),
        metavar="FORMAT",
    )
    parser.add_argument("--debug", action="store_true", help="Print debug info.")
    parser.add_argument("-V", "--version", action="version", version=__version__)
    return parser


def is_valid_path(path: str) -> bool:
    """Check if a file path is valid."""
    if not os.path.exists(path):
        logger.error("no such file or directory: %s", repr(path))
        return False
    if not os.path.isfile(path):
        logger.error("not a valid input file: %s", repr(path))
        return False
    return True


def main(argv: Sequence[str] | None = None) -> int:
    """Check cli arguments."""
    args = build_parser().parse_args(argv)

    log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S",
        level=log_level,
    )

    if not is_valid_path(args.syntax):
        return 2

    ins: list[Path] = []
    outs: list[Path] = []
    for f in args.filename:
        if not is_valid_path(f):
            return 2
        path, _ = os.path.splitext(f)
        ins.append(Path(f))
        outs.append(Path(f"{path}.{args.format.lower()}"))

    start = datetime.datetime.now()
    convert_files(Path(args.syntax), ins, outs, args.format)
    logger.debug("Total: %s", str(datetime.datetime.now() - start))
    return 0
