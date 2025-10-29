"""Module defining base writer class."""

import yaml
from .json import Json, JsonType


class Yaml(Json):
    """Base writer class."""

    def generate_output(self) -> str:
        """Generate output in specified format."""
        if self.root_name != "root":
            self.root.name = self.root_name
        tree: JsonType | list[JsonType] = self.serialize_node(self.root)
        return yaml.dump(tree)
