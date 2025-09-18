"""Utility functions."""

import datetime
import logging

from .compiler.compiler import Compiler
from .processor.context import Context
from .processor.processor import Processor
from .writer import json, xml, yaml

logger = logging.getLogger(__name__)


def convert_files(
    syntax_file: str,
    input_files: list[str],
    output_files: list[str],
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
    match output_format:
        case "json":
            writer_cls = json.Json
        case "xml":
            writer_cls = xml.Xml
        case "yaml":
            writer_cls = yaml.Yaml
        case _:
            raise ValueError(f"Unsupported output format {output_format}")
    start = datetime.datetime.now()
    syntax = Compiler().compile_file(syntax_file)
    logger.debug("Compiled syntax in %s", str(datetime.datetime.now() - start))
    for input_file, output_file in zip(input_files, output_files):
        content = open(input_file, "r", encoding=encoding).read()
        context = Context(content, writer_cls)
        processor = Processor(context, syntax)
        processor.convert()
        context.writer.write_to(output_file, encoding)


def convert_file(
    syntax_file: str,
    input_file: str,
    output_file: str,
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
