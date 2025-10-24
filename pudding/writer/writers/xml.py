"""Module defining xml writer class."""

from pathlib import Path
from typing import Any

from lxml import etree

from ..node import Node
from .writer import Writer, BufferedWriter


class SliXml(Writer):
    """Writer class for slim xml output."""

    def __init__(
        self, file_path: Path, root_name: str = "xml", encoding: str = "utf-8"
    ) -> None:
        """Init for SliXml class."""
        super().__init__(file_path, root_name, encoding)
        self.indent = 0
        self.file = open(file_path, "w", encoding=encoding)
        self.prev_roots: list[str] = []
        self.prev_indents: list[int] = []
    
    def _writeline(self, line: str) -> None:
        """Write line with indent to output."""
        self.file.write(f"{'  '*self.indent}{line}\n")

    def _to_tag(
        self,
        name: str,
        attributes: dict[str, str],
        value: str | None = None,
        open: bool = False,
    ) -> str:
        """Create an xml tag.

        :param name: Name of the tag.
        :param attributes: Attributes of the tag.
        :param value: Text of this tag.
        :param open: If no value is set, this determines if a tag is closed or not.
        :returns str: XML-Tag as a string.
        """
        tag = name.casefold()
        attribs = [f' {k}="{v}"' for k, v in attributes.items()]
        xml = f"<{tag}{''.join(attribs)}"
        if value is not None:
            return f"{xml}>{value}<{tag}/>"
        return f"{xml}{'/'*(not open)}>"

    def add_attribute(self, path: str, name: str, value: str) -> None:
        raise NotImplementedError

    def create_element(self, path: str, value: str | None = None) -> Any:
        """Add an element to the current node.

        :param path: Path of the element.
        :param value: Value of the element or None if it has no value.
        :returns: The created element.
        """
        paths = Node.split_path(path)
        if len(paths) == 1:
            name, attribs = Node.parse_node_path(paths[0][0])
            self._writeline(self._to_tag(name, attribs, value))
            return
        for node in paths[:-1]:
            name, attribs = Node.parse_node_path(node[0])
            self._writeline(self._to_tag(name, attribs, open=True))
        name, attribs = Node.parse_node_path(paths[-1][0])
        self._writeline(self._to_tag(name, attribs, value))
        for node in reversed(paths[:-1]):
            self._writeline(f"<{node[2]}/>")

    def add_element(self, path: str, value: str | None = None) -> Any:
        """Add an element if it not already exists.

        Otherwise it appends the string to the already existing element.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        :returns: The created element.
        """
        return self.create_element(path, value)

    def enter_path(self, path: str, value: str | None = None) -> None:
        """Enter a node and create elements in the path if they do not already exist.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        paths = Node.split_path(path)
        for node in paths:
            self.prev_indents.append(self.indent)
            name, attribs = Node.parse_node_path(node[0])
            self.prev_roots.append(name)
            self._writeline(self._to_tag(name, attribs, open=True))
            self.indent += 1

    def open_path(self, path: str, value: str | None = None) -> None:
        """Enter a node and create elements in the path if they do not already exist.

        Always creates the last node.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        return self.enter_path(path, value)

    def leave_path(self) -> None:
        """Leave the previously entered path."""
        self.indent = self.prev_indents.pop()
        closing_tag = self.prev_roots.pop()
        self._writeline(f"<{closing_tag}/>")

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
        raise NotImplementedError

    def write_to(self, encoding: str = "utf-8") -> None:
        """Write generated output to file.

        :param file_path: Path of the file to write to.
        """
        raise NotImplementedError


class Xml(BufferedWriter):
    """Writer class for xml output."""

    def __init__(
        self, file_path: Path, root_name: str = "xml", encoding: str = "utf-8"
    ) -> None:
        super().__init__(file_path, root_name, encoding)

    def serialize_node(self, node: Node) -> etree.Element:
        root = etree.Element(node.name, node.attribs)
        root.text = node.text
        for child in node.children:
            root.append(self.serialize_node(child))
        return root

    def generate_output(self) -> str:
        """Generate output in specified format."""
        self.root.name = self.root_name
        tree = self.serialize_node(self.root)
        return etree.tostring(tree, pretty_print=True, encoding=str)

    def write_to(self, encoding: str = "utf-8") -> None:
        """Write generated output to file.

        :param file_path: Path of the file to write to.
        """
        self.root.name = self.root_name
        tree = etree.ElementTree(self.serialize_node(self.root))
        return tree.write(
            self.file_path, encoding=encoding, pretty_print=True, xml_declaration=False
        )
