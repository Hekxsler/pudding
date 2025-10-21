"""Module defining base writer class."""

import yaml
from .json import Json


class Yaml(Json):
    """Base writer class."""

    def generate_output(self) -> str:
        """Generate output in specified format."""
        return yaml.dump(self.tree)
