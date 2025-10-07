"""Main script."""

import argparse
import datetime
import logging
import os

from argparse import ArgumentError
from pudding import convert_files

DESCRIPTION = """
Pudding converts text to a structured format, such as XML, JSON or YAML.
"""
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument("filename", help="The file or files to convert.", nargs="+")
parser.add_argument(
    "-s",
    "--syntax",
    default=None,
    help="The file containing the syntax for parsing the input.",
    metavar="FILE",
    required=True,
)
parser.add_argument(
    "-f",
    "--format",
    choices=["xml", "json", "yaml", "none"],
    default="xml",
    help="The output format.",
    metavar="FORMAT",
)
parser.add_argument("--debug", action="store_true", help="Print debug info.")


def main() -> None:
    """Script function."""
    args = parser.parse_args()
    log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S",
        level=log_level,
    )
    logger = logging.getLogger(__name__)

    if not os.path.exists(args.syntax):
        raise ArgumentError(None, f"no such file or directory: {repr(args.syntax)}")
    if not os.path.isfile(args.syntax):
        raise ArgumentError(None, f"not a valid input file: {repr(args.syntax)}")

    start = datetime.datetime.now()
    outs: list[str] = []
    for f in args.filename:
        if not os.path.exists(f):
            raise ArgumentError(None, f"no such file or directory: {repr(f)}")
        if not os.path.isfile(f):
            raise ArgumentError(None, f"not a valid input file: {repr(f)}")
        path, _ = os.path.splitext(f)
        outs.append(f"{path}.{args.format.lower()}")
    convert_files(args.syntax, args.filename, outs, args.format)
    logger.debug("Total: %s", str(datetime.datetime.now() - start))

if __name__ == "__main__":
    main()
