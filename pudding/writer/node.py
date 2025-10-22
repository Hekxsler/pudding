"""Node class for caching generated output."""

import re
from functools import lru_cache
from typing import Iterator, Self


class Node:
    """Class representing a node."""

    attribute_re = re.compile(r'([?&]([\w\-\_]+)="((?:\\\"|[^"])+)")')
    node_re = re.compile(rf'((?:(\.)|(\/?)([\w\-\_ ]+)({attribute_re.pattern}*)))')

    def __init__(
        self, name: str, attributes: dict[str, str] | None = None, text: str | None = None
    ) -> None:
        """Init for Node class.

        :param name: Name of this node.
        :param attributes: Attributes of this node.
        :param text: Text value of this node.
        """
        self.name = name
        # avoid mutable default arguments
        self.attribs = {} if attributes is None else attributes
        self.children: list[Self] = []
        self.text = text

    @classmethod
    def from_path(cls, path: str, text: str | None = None) -> Self:
        """Parse node object from path.

        :param path: Node path of the object.
        :param text: Text of the created node object.
        :returns Node: The created node object.
        """
        name, attribs = cls.parse_node_path(path)
        return cls(name, attribs, text)

    @classmethod
    def parse_node_path(cls, path: str) -> tuple[str, dict[str, str]]:
        """Read tag name and attributes from an node.

        :param path: Path node to parse.
        :returns: Tuple with name as string and attributes as a dict.
        """
        # Use a cached helper to avoid repeated regex parsing for the same path
        name, items = _parse_node_path_cached(path)
        return name, dict(items)

    @classmethod
    def split_path(cls, path: str) -> list[tuple[str, str, str, str]]:
        """Split the path into nodes.

        :param path: Path to split.
        :returns: List of node matches as a tuple.
            E.g. [(full_nodepath, [./]*, tag, attributes), ...]
        """
        # cache split results as tuple for lru_cache and return a list
        return list(_split_path_cached(path))

    def iter_children(self) -> Iterator[Self]:
        """Return iterator of childrens."""
        return iter(self.children)

    def add_child(self, node: Self) -> None:
        """Create a child node of this node.

        :param name: Name of the child node.
        :param attributes: Attributes of the child node.
        :returns: The child node.
        """
        self.children.append(node)

    def find(self, path: str) -> Self | None:
        """Find a child in the given path.

        :param path: Path to the node.
        :returns: The node or None if it does not exist.
        """
        if path == ".":
            return self
        if not self.children:
            return None
        root = self
        for node_path in self.split_path(path):
            tag, attribs = self.parse_node_path(node_path[0])
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
        return self.attribs.get(name, default)

    def __repr__(self) -> str:
        return f"<Node name={repr(self.name)} {self.attribs} children={self.children}>"


@lru_cache(maxsize=20000)
def _parse_node_path_cached(path: str) -> tuple[str, tuple[tuple[str, str], ...]]:
    """Cached parser for a single node path. Returns (name, tuple(items)).

    Keeping the cached value immutable avoids accidental mutation in cache.
    """
    attributes: dict[str, str] = {}
    p = path.lstrip("./")
    for attribute in Node.attribute_re.findall(p):
        attributes[attribute[1]] = attribute[2]
        p = p.replace(attribute[0], "")
    if "/" in p:
        raise ValueError(f"Path {p} contains more than one node.")
    p = p.replace(" ", "-")
    return p.casefold(), tuple(sorted(attributes.items()))


@lru_cache(maxsize=20000)
def _split_path_cached(path: str) -> tuple[tuple[str, str, str, str], ...]:
    return tuple(Node.node_re.findall(path))
