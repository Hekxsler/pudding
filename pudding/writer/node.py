"""Node class for caching generated output."""

import re
from typing import Self


class Node:
    """Class representing a node."""

    attribute_re = re.compile(r"([?&]([\w\-\_]+)=\"((?:\\\"|[^\"])+)\")")
    node_re = re.compile(rf"((?:(\.)|(\/?)([\w\-\_ ]+)({attribute_re.pattern}*)))")

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
        self.children: dict[str, list[Self]] = {}
        self.text = text
        self.parent: Self | None = None

    def __eq__(self, other: object) -> bool:
        """Compare Node object to other object.

        To equal only name and attributes have to be the same.
        Text and children of the nodes are ignored.
        """
        if not isinstance(other, Node):
            return False
        if self.name == other.name and self.attribs == other.attribs:
            return True
        return False

    @classmethod
    def from_path(cls, path: str, text: str | None = None) -> Self:
        """Parse node object from path.

        :param path: Node path of the object.
        :param text: Text of the created node object.
        :returns Node: The created node object.
        """
        return cls(*cls.parse_node_path(path), text)

    @classmethod
    def parse_node_path(cls, path: str) -> tuple[str, dict[str, str]]:
        """Read tag name and attributes from an node.

        :param path: Path node to parse.
        :returns: Tuple with name as string and attributes as a dict.
        """
        attributes: dict[str, str] = {}
        path = path.lstrip("./")
        for attribute in cls.attribute_re.findall(path):
            attributes[attribute[1]] = attribute[2]
            path = path.replace(attribute[0], "")
        if "/" in path:
            raise ValueError(f"Path {path} contains more than one node.")
        path = path.replace(" ", "-")
        return path.casefold(), attributes

    @classmethod
    def split_path(cls, path: str) -> list[tuple[str, str, str, str]]:
        """Split the path into nodes.

        :param path: Path to split.
        :returns: List of node matches as a tuple.
            E.g. [(full_nodepath, [./]*, tag, attributes), ...]
        """
        return cls.node_re.findall(path)

    def add_child(self, node: Self) -> None:
        """Create a child node of this node.

        :param name: Name of the child node.
        :param attributes: Attributes of the child node.
        :returns: The child node.
        """
        node.parent = self
        childs = self.children.get(node.name, [])
        self.children[node.name] = childs + [node]

    def find(self, path: str) -> Self | None:
        """Find a child in the given path.

        :param path: Path to the node.
        :returns: The node or None if it does not exist.
        """
        if path == ".":
            return self
        if len(self.children) == 0:
            return None
        root = self
        for tag, attribs in (
            self.parse_node_path(path[0]) for path in self.split_path(path)
        ):
            found = False
            for child in root.children.get(tag, []):
                if tag != child.name:
                    continue
                if attribs != child.attribs:
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
        return self.attribs.get(name, default)

    def __repr__(self) -> str:
        return f"<Node name={repr(self.name)} {self.attribs} children={self.children}>"
