"""Package for writing output."""

from .writers.json import Json
from .writers.writer import Writer

__all__ = ["Json", "Writer"]
available_writers: list[type[Writer]] = [Json, Writer]

try:
    from .writers.xml import SliXml, Xml

    __all__.extend(["SliXml", "Xml"])
    available_writers.extend([SliXml, Xml])
except ImportError:
    pass

try:
    from .writers.yaml import Yaml

    __all__.append("Yaml")
    available_writers.append(Yaml)
except ImportError:
    pass
