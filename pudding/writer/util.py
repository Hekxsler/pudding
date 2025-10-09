"""Utility functions for writer package."""

from .yaml import Yaml
from .xml import Xml
from .json import Json
from .writer import Writer


def get_writer_from_format(format: str) -> type[Writer]:
    """Return writer class for a format."""
    match format:
        case "json":
            return Json
        case "xml":
            return Xml
        case "yaml":
            return Yaml
        case _:
            raise ValueError(f"Unsupported format {format}")
