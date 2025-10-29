"""Module defining xml writer class."""

from pathlib import Path

from lxml import etree

from ..node import Node
from .writer import BufferedWriter, Writer


class SliXml(Writer):
    """Writer class for slim xml output."""

    def __init__(
        self, file_path: Path, root_name: str = "xml", encoding: str = "utf-8"
    ) -> None:
        """Init for SliXml class."""
        super().__init__(file_path, root_name, encoding)
        self.last_open = True
        self.last_indent = 0
        self.indent = 1
        self.file = open(file_path, "w", encoding=encoding)
        self.last_node: Node = Node(root_name)
        self.prev_roots: list[str] = []
        self.prev_indents: list[int] = []

    def _writenode(self, node: Node, open: bool = False) -> None:
        """Write node to file."""
        self._writeline(
            self._to_tag(
                self.last_node.name,
                self.last_node.attribs,
                self.last_node.text,
                open=self.last_open,
            )
        )
        self.last_indent = self.indent
        self.last_node = node
        self.last_open = open

    def _writeline(self, line: str) -> None:
        """Write line with indent to output."""
        self.file.write(f"{'  '*self.last_indent}{line}\n")

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
        if path != ".":
            msg = "Can only edit current tag when using slixml writer."
            raise ValueError(f"Invalid path {repr(path)}. {msg}")
        self.last_node.attribs[name] = value

    def create_element(self, path: str, value: str | None = None) -> None:
        """Add an element to the current node.

        :param path: Path of the element.
        :param value: Value of the element or None if it has no value.
        """
        paths = Node.split_path(path)
        if len(paths) == 1:
            self._writenode(Node.from_path(paths[0][0], value))
            return
        for node in paths[:-1]:
            self._writenode(Node.from_path(node[0], value), True)
        self._writenode(Node.from_path(paths[-1][0], value))
        for node in reversed(paths[:-1]):
            self._writenode(Node.from_path(node[2], value))

    def add_element(self, path: str, value: str | None = None) -> None:
        """Add an element if it not already exists.

        Otherwise it appends the string to the already existing element.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        if self.last_node == Node.from_path(path):
            if not value:
                return
            if not self.last_node.text:
                self.last_node.text = value
            else:
                self.last_node.text += value
        else:
            self.create_element(path, value)

    def enter_path(self, path: str, value: str | None = None) -> None:
        """Enter a node and create elements in the path if they do not already exist.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        paths = Node.split_path(path)
        for node in paths:
            name, attribs = Node.parse_node_path(node[0])
            self._writenode(Node(name, attribs, value), open=True)
            self.prev_roots.append(name)
            self.prev_indents.append(self.indent)
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
        self._writenode(Node(closing_tag))


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
