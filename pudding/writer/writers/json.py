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
    return elem


class Json(BufferedWriter):
    """Writer class for json output."""

    def serialize_node(self, node: Node) -> JsonType:
        if len(node.children) == 0:
            return {node.name: _to_json(node)}
        elems = [_to_json(node)]
        for child in node.children:
            elems.append(self.serialize_node(child))
        return {node.name: elems}

    def generate_output(self) -> str:
        """Generate output in specified format."""
        if self.root_name != "root":
            self.root.name = self.root_name
        tree: JsonType | list[JsonType] = self.serialize_node(self.root)
        return json.dumps(tree, indent=4)
