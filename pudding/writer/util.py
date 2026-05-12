"""Utility functions for writer package."""

from . import __all__, available_writers
from .writers.writer import Writer


def get_writer_from_format(output_format: str) -> type[Writer]:
    """Return writer class for a output format."""
    for name, cls in zip(__all__, available_writers):
        if output_format.lower() == name.lower():
            return cls
    raise ValueError(f"Unsupported output format {output_format}.")
