"""Node class for caching generated output."""

import re
from typing import Iterator, Self

ATTRIBUTE_RE = re.compile(r"([?&]([\w\-\_]+)=\"((?:\\\"|[^\"])+)\")")
NODE_RE = re.compile(rf"((\.?\/?)([\w\-\_ ]+)({ATTRIBUTE_RE}*))")


def split_path(path: str) -> list[tuple[str, str, str, str]]:
    """Split the path into nodes.

    :param path: Path to split.
    :returns: List of node matches as a tuple.
        E.g. [(full_nodepath, [./]*, tag, attributes), ...]
    """
    return NODE_RE.findall(path)


def parse_node_path(path: str) -> tuple[str, dict[str, str]]:
    """Read tag name and attributes from an node.

    :param path: Path node to parse.
    :returns: Tuple with name as string and attributes as a dict.
    """
    attributes: dict[str, str] = {}
    path = path.lstrip("./")
    for attribute in ATTRIBUTE_RE.findall(path):
        attributes[attribute[1]] = attribute[2]
        path = path.replace(attribute[0], "")
    if "/" in path:
        raise ValueError("Given path is not a node.")
    path = path.replace(" ", "-")
    return path.casefold(), attributes


class Node:
    """Class representing a node."""

    def __init__(
        self, name: str, attributes: dict[str, str] = {}, text: str | None = None
    ) -> None:
        """Init for Node class.

        :param name: Name of this node.
        :param attributes: Attributes of this node.
        :param text: Text value of this node.
        """
        self.name = name
        self.attribs = attributes
        self.children: list[Self] = []
        self.text = text

    def iter_children(self) -> Iterator[Self]:
        """Return iterator of childrens."""
        return self.children.__iter__()

    def add_child(self, name: str, attributes: dict[str, str] = {}) -> Self:
        """Create a child node of this node.

        :param name: Name of the child node.
        :param attributes: Attributes of the child node.
        :returns: The child node.
        """
        child = self.__class__(name, attributes)
        self.children.append(child)
        return child

    def find(self, path: str) -> Self | None:
        """Find a child in the given path.

        :param path: Path to the node.
        """
        if path == ".":
            return self
        root = self
        for node_path in split_path(path):
            tag, attribs = parse_node_path(node_path[0])
            found = False
            for child in root.iter_children():
                if child.name != tag:
                    continue
                if child.attribs != attribs:
                    continue
                root = child
                found = True
                break
            if not found:
                return None
        return root

    def set(self, name: str, value: str) -> None:
        """Set an attribute of this node.

        :param name: Name of the attribute.
        :param value: Value of the attribute.
        """
        self.attribs[name] = value

    def get(self, name: str, default: None = None) -> str | None:
        """Get an attribute of this node.

        :param name: Name of the attribute.
        """
        self.attribs.get(name, default)
