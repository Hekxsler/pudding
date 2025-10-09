"""Module defining base writer class."""

from pathlib import Path
import re
from typing import Any

from . import NODE_ATTRIBUTE_RE, NODE_RE


class Writer:
    """Base writer class.

    :var attrib_re: Regex for node attributes.
    :var node_re: Regex for a node path.
    """

    attrib_re = re.compile(NODE_ATTRIBUTE_RE)
    node_re = re.compile(NODE_RE)

    def __init__(self, root_name: str | None = None) -> None:
        """Init function for base Writer class.

        :param root_name: Name of the root element.
        """
        self.root_name = root_name

    def _split_path(self, path: str) -> list[tuple[str, ...]]:
        """Split the path."""
        return self.node_re.findall(path)

    def _parse_node(self, path: str) -> tuple[str, dict[str, str]]:
        """Read tag name and attributes from an node.

        :param path: Path node to parse.
        :returns: Tuple with name as string and attributes as a dict.
        """
        attributes: dict[str, str] = {}
        path = path.lstrip("./")
        for attribute in self.attrib_re.findall(path):
            attributes[attribute[1]] = attribute[2]
            path = path.replace(attribute[0], "")
        if "/" in path:
            raise ValueError("Given path is not a node.")
        path = path.replace(" ", "-")
        return path.casefold(), attributes

    def add_attribute(self, path: str, name: str, value: str) -> None:
        """Add an attribute to an element.

        :param path: Path of the element.
        :param name: Name of the attribute.
        :param value: Value of the attribute.
        """
        raise NotImplementedError

    def create_element(self, path: str, value: str | None = None) -> Any:
        """Add an element to the current node.

        :param path: Path of the element.
        :param value: Value of the element or None if it has no value.
        """
        raise NotImplementedError

    def add_element(self, path: str, value: str | None = None) -> Any:
        """Adds an element if it not already exists.

        Otherwise it appends the string to the already existing element.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        raise NotImplementedError

    def enter_path(self, path: str, value: str | None = None) -> None:
        """Enter a node and create elements in the path if they do not already exist.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        raise NotImplementedError

    def open_path(self, path: str, value: str | None = None) -> None:
        """Enter a node and create elements in the path if they do not already exist.

        Always creates the last node.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        raise NotImplementedError

    def leave_path(self) -> None:
        """Leave the previously entered path."""
        raise NotImplementedError

    def delete_element(self, path: str) -> None:
        """Delete an element.

        :param path: Path of the element.
        """
        raise NotImplementedError

    def replace_element(self, path: str, value: str | None = None) -> None:
        """Replace an element.

        :param path: Path of the element.
        :param value: Value of the replaced element or None if it has no value.
        """
        raise NotImplementedError

    def generate_output(self) -> str:
        """Generate output in specified format."""
        raise NotImplementedError

    def print_output(self) -> None:
        """Print output to stdout."""
        print(self.generate_output())

    def write_to(self, file_path: Path, encoding: str = "utf-8") -> None:
        """Write generated output to file.

        :param file_path: Path of the file to write to.
        """
        with open(file_path, "w", encoding=encoding) as f:
            f.write(self.generate_output())
