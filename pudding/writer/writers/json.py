"""Module defining json writer class."""

import json

from .writer import BufferedWriter
from ..node import Node

type JsonType = dict[str, JsonType | list[JsonType] | str]


def _to_json(node: Node) -> JsonType:
    """Create a json type objects from node.

    :param node: Node object to convert.
    :returns: The JsonType object.
    """
    elem: JsonType = {}
    for k, v in node.attribs.items():
        elem[f"@{k}"] = v
    if node.text is not None:
        elem["#text"] = node.text
    for child in node.get_sorted_children():
        existing = elem.get(child.name)
        if isinstance(existing, str):
            raise RuntimeError
        if not existing:
            elem[child.name] = _to_json(child)
            continue
        if not isinstance(existing, list):
            existing = [existing]
        existing.append(_to_json(child))
        elem[child.name] = existing
    return elem


class Json(BufferedWriter):
    """Writer class for json output."""

    def serialize_node(self, node: Node, parent: JsonType) -> JsonType:
        """Convert node object to json."""
        existing = parent.get(node.name)
        if isinstance(existing, str):
            raise RuntimeError
        if not existing:
            parent[node.name] = _to_json(node)
            return parent
        if not isinstance(existing, list):
            existing = [existing]
        existing.append(_to_json(node))
        parent[node.name] = existing
        return parent

    def generate_output(self) -> str:
        """Generate output in specified format."""
        base: JsonType = {}
        for child in self.root.get_sorted_children():
            base = self.serialize_node(child, base)
        return json.dumps(base, indent=4)
