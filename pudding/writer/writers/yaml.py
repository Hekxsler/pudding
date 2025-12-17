"""Module defining base writer class."""

import yaml
from .json import Json, JsonType


class Yaml(Json):
    """Base writer class."""

    def generate_output(self) -> str:
        """Generate output in specified format."""
        base: JsonType = {}
        for child in self.root.get_sorted_children():
            base = self.serialize_node(child, base)
        return yaml.dump(base)
