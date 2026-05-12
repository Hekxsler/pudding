"""Main script."""

import argparse
import datetime
import logging
import os
from collections.abc import Sequence
from pathlib import Path

from .util import convert_files
from .version import __version__
from .writer import __all__ as format_choices

DEFAULT_FORMAT = "json"
DESCRIPTION = """
Pudding converts text to a structured format, such as XML, JSON or YAML.
For more information see the documentation at https://pudding.readthedocs.io/latest.
"""

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser."""
    parser = argparse.ArgumentParser(prog="pudding", description=DESCRIPTION)
    parser.add_argument(
        "filename", help="The file or files to convert.", metavar="FILE", nargs="+"
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
        choices=format_choices,
        default=DEFAULT_FORMAT,
        help=(
            "The output format. "
            f"Choices are: {', '.join(format_choices)}. Default is `{DEFAULT_FORMAT}`."
        ),
        metavar="FORMAT",
    )
    parser.add_argument(
        "-o",
        "--output",
        help=(
            "If converting a single file this is the name of the output file. "
            "When converting multiple files this is the output directory."
        ),
        metavar="OUTPUT",
    )
    parser.add_argument("--debug", action="store_true", help="Print debug info.")
    parser.add_argument("-V", "--version", action="version", version=__version__)
    return parser


def is_valid_inpath(path: str) -> bool:
    """Check if a syntax file path is valid."""
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

    if not is_valid_inpath(args.syntax):
        return 2

    ins: list[Path] = []
    outs: list[Path] = []
    if len(args.filename) == 1:
        f = args.filename[0]
        if not is_valid_inpath(f):
            return 2
        path, _ = os.path.splitext(f)
        ins.append(Path(f))
        if args.output:
            outs.append(Path(args.output))
        else:
            outs.append(Path(f"{path}.{args.format.lower()}"))
    else:
        for f in args.filename:
            if not is_valid_inpath(f):
                return 2
            path, _ = os.path.splitext(f)
            ins.append(Path(f))
            output_path = Path(f"{path}.{args.format.lower()}")
            if args.output:
                outs.append(Path(args.output) / output_path)
            else:
                outs.append(output_path)

    start = datetime.datetime.now()
    try:
        convert_files(Path(args.syntax), ins, outs, args.format)
    except ValueError as e:
        logger.error(e)
    logger.debug("Total: %s", str(datetime.datetime.now() - start))
    return 0
