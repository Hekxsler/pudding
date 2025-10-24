"""Utility functions for writer package."""

from .writers.json import Json
from .writers.writer import Writer
from .writers.xml import SliXml, Xml
from .writers.yaml import Yaml


def get_writer_from_format(format: str) -> type[Writer]:
    """Return writer class for a format."""
    match format:
        case "slixml":
            return SliXml
        case "json":
            return Json
        case "xml":
            return Xml
        case "yaml":
            return Yaml
        case _:
            raise ValueError(f"Unsupported format {format}")
