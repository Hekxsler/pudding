"""Module defining xml writer class."""

from pathlib import Path

from lxml import etree

from ..node import Node
from .writer import Writer


class Xml(Writer):
    """Writer class for xml output."""

    def __init__(self, root_name: str = "xml") -> None:
        super().__init__(root_name)

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

    def write_to(self, file_path: Path, encoding: str = "utf-8") -> None:
        """Write generated output to file.

        :param file_path: Path of the file to write to.
        """
        self.root.name = self.root_name
        tree = etree.ElementTree(self.serialize_node(self.root))
        return tree.write(
            file_path, encoding=encoding, pretty_print=True, xml_declaration=False
        )
