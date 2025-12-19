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
        self.last_single = False
        self.last_closing = False
        self.last_indent = 0
        self.indent = 1
        self.file = open(file_path, "w", encoding=encoding)
        self.last_node: Node = Node(root_name)
        self.prev_roots: list[str] = [root_name]

    def _writenode(self, node: Node, single: bool = False, closing: bool = False) -> None:
        """Write node to file."""
        self._writeline(
            self._to_tag(
                self.last_node.name,
                self.last_node.attribs,
                self.last_node.text,
                single=self.last_single,
                closing=self.last_closing,
            )
        )
        self.last_indent = self.indent
        self.last_node = node
        self.last_single = single
        self.last_closing = closing

    def _writeline(self, line: str) -> None:
        """Write line with indent to output."""
        self.file.write(f"{'  '*self.last_indent}{line}\n")

    def _to_tag(
        self,
        name: str,
        attributes: dict[str, str],
        value: str | None = None,
        single: bool = False,
        closing: bool = False,
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
        xml = f"{tag}{''.join(attribs)}"
        if value is not None:
            return f"<{xml}>{value}</{tag}>"
        return f"<{'/'*(closing)}{xml}{'/'*(single and not closing)}>"

    def create_element(self, path: str, value: str | None = None) -> None:
        """Add an element to the current node.

        :param path: Path of the element.
        :param value: Value of the element or None if it has no value.
        """
        paths = Node.split_path(path)
        match len(paths):
            case 0:
                raise ValueError(f"Invalid path {repr(path)}.")
            case 1:
                node = Node.from_path(paths[0][0], value)
                self._writenode(node, single=True)
            case _:
                for node in paths[:-1]:
                    self._writenode(Node.from_path(node[0], value))
                self._writenode(Node.from_path(paths[-1][0], value), single=True)
                for node in reversed(paths[:-1]):
                    self._writenode(Node.from_path(node[2], value), closing=True)

    def add_element(self, path: str, value: str | None = None) -> None:
        """Add an element if its not the current element.

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
        """Enter a node and create elements in the path.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        paths = Node.split_path(path)
        for node_path, _, _, _ in paths:
            self._writenode(Node.from_path(node_path))
            self.indent += 1
        self.last_node.text = value
        self.prev_roots.append("/".join([p[2] for p in paths]))

    def open_path(self, path: str, value: str | None = None) -> None:
        """Enter a node and create elements in the path.

        Always creates the last node.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        return self.enter_path(path, value)

    def leave_paths(self, amount: int = 1) -> None:
        """Leave the previously entered path."""
        for _ in range(amount):
            last_root = self.prev_roots.pop()
            for node in reversed(last_root.split("/")):
                self.indent -= 1
                self._writenode(Node(node), closing=True)

    def write_output(self) -> None:
        """Write last open nodes to file."""
        self.leave_paths(len(self.prev_roots))
        # write last node again because it buffers the last node
        self._writenode(self.last_node, closing=True)


class Xml(BufferedWriter):
    """Writer class for xml output."""

    def __init__(
        self, file_path: Path, root_name: str = "xml", encoding: str = "utf-8"
    ) -> None:
        """Init buffered xml writer."""
        super().__init__(file_path, root_name, encoding)

    def serialize_node(self, node: Node) -> etree.Element:
        """Convert node object to etree element."""
        root = etree.Element(node.name, node.attribs)
        root.text = node.text
        for child in node.get_sorted_children():
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
