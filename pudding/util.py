"""Utility functions."""

import datetime
import logging
from pathlib import Path

from .writer.util import get_writer_from_format

from .compiler.compiler import Compiler
from .processor.context import Context
from .processor.processor import Processor

logger = logging.getLogger(__name__)


def convert_files(
    syntax_file: Path,
    input_files: list[Path],
    output_files: list[Path],
    output_format: str,
    encoding: str = "utf-8",
) -> None:
    """Convert multiple files.

    :param syntax_file: Path of the ".pud" file.
    :param input_files: List of file paths to convert.
    :param output_file:
        List of paths to write to, where the index corresponds to index of the
        input filepaths. E.g. the converted output of the first file in `input_files`
        will be written to the first path in this list.
    :param output_format: Format of the output.
    :param encoding: Encoding of the input and output files.
    """
    start = datetime.datetime.now()
    syntax = Compiler().compile_file(syntax_file)
    logger.debug("Compiled syntax in %s", str(datetime.datetime.now() - start))
    writer_cls = get_writer_from_format(output_format)
    for input_file, output_file in zip(input_files, output_files):
        content = open(input_file, "r", encoding=encoding).read()
        context = Context(content, writer_cls)
        writer = Processor(context, syntax).convert()
        writer.write_to(output_file, encoding)


def convert_file(
    syntax_file: Path,
    input_file: Path,
    output_file: Path,
    output_format: str,
    encoding: str = "utf-8",
) -> None:
    """Convert a single file.

    :param syntax_file: Path of the ".pud" file.
    :param input_file: Path of the file to convert.
    :param output_file: Path of the file to write to.
    :param output_format: Format of the output.
    :param encoding: Encoding of the input and output file.
    """
    return convert_files(
        syntax_file, [input_file], [output_file], output_format, encoding
    )


def convert_string(syntax: str, input: str, output_format: str) -> str:
    """Convert a string.

    :param syntax: Content of a ".pud" file.
    :param input: String to convert.
    :param output_format: Format of the output.
    """
    start = datetime.datetime.now()
    compiler = Compiler().compile(syntax)
    logger.debug("Compiled syntax in %s", str(datetime.datetime.now() - start))
    writer_cls = get_writer_from_format(output_format)
    context = Context(input, writer_cls)
    writer = Processor(context, compiler).convert()
    return writer.generate_output()
