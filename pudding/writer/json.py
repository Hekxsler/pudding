"""Module defining json writer class."""

import json

from .writer import Writer

type JsonType = dict[str, JsonType | list[JsonType] | str]


def _add_element(parent: JsonType, tag: str, child: JsonType) -> JsonType:
    """Add a child element to a parent.

    :param parent: The parent element.
    :param tag: Tag of the child element.
    :param child: The child element to add.
    :returns: The child element.
    """
    children = parent.get(tag)
    if children is None:
        children = child
    elif isinstance(children, dict):
        children = [children, child]
    elif isinstance(children, list):
        children.append(child)
    parent[tag] = children
    return child


def _to_json(attribs: dict[str, str], text: str | None = None) -> JsonType:
    """Create a json type objects from attributes and text.

    :param attribs: Attributes of the json object.
    :param text: Text of the object or None if it has no text.
    :returns: The JsonType object.
    """
    elem: JsonType = {}
    for k, v in attribs.items():
        elem[f"@{k}"] = v
    if text is not None:
        elem["#text"] = text
    return elem


def _filter_attr(elems: list[JsonType], attribs: dict[str, str]) -> JsonType | None:
    """Filter a list of json objects by attributes and return the first matching.

    An object must have the exact same attributes.

    :param elems: The list to filter.
    :param attribs: Attributes to filter by.
    :returns: The object or None if none matched.
    """
    for elem in elems:
        found = True
        for k, v in elem.items():
            if not k.startswith("@"):
                continue
            k = k.lstrip("@")
            if not v == attribs.get(k):
                found = False
                break
        if found:
            return elem
    return None


class Json(Writer):
    """Writer class for json output."""

    tree: JsonType = {}
    prev_roots: list[JsonType] = []

    def __init__(self) -> None:
        """Init for Json writer class."""
        self.root = self.tree
        super().__init__()

    def _get_element(self, path: str) -> JsonType:
        """Return the element at the given path.

        :param path: Pudding path to the element.
        :returns: The JsonType object.
        :raises ValueError: If path is invalid.
        """
        start_elem = self.root
        for sub_path in self._split_path(path):
            tag, attribs = self._parse_node(sub_path[0])
            sub_elements = start_elem.get(tag, [])
            if isinstance(sub_elements, str):
                raise KeyError(f"Path {path} leads to an attribute.")
            if isinstance(sub_elements, dict):
                sub_elements = [sub_elements]
            sub_elem = _filter_attr(sub_elements, attribs)
            if sub_elem is not None:
                start_elem = sub_elem
                continue
            new_elem = _to_json(attribs)
            start_elem = _add_element(start_elem, tag, new_elem)
        return start_elem

    def _get_or_create_element(self, path: str) -> JsonType:
        """Return the element at the given path and create missing elements.

        :param path: Pudding path to the element.
        :returns: The JsonType object.
        """
        start_elem = self.root
        for sub_path in self._split_path(path):
            tag, attribs = self._parse_node(sub_path[0])
            sub_elements = start_elem.get(tag, [])
            if isinstance(sub_elements, str):
                raise KeyError(f"Path {path} leads to an attribute.")
            if isinstance(sub_elements, dict):
                sub_elements = [sub_elements]
            sub_elem = _filter_attr(sub_elements, attribs)
            if sub_elem is None:
                raise KeyError(f"Element at path {path} does not exist")
            start_elem = sub_elem
        return start_elem

    def add_attribute(self, path: str, name: str, value: str) -> None:
        """Add an attribute to an element.

        :param path: Path of the element.
        :param name: Name of the attribute.
        :param value: Value of the attribute.
        """
        self._get_element(path)[f"@{name}"] = value

    def create_element(self, path: str, value: str | None = None) -> JsonType:
        """Add an element to the current node.

        :param path: Path of the element.
        :param value: Value of the element or None if it has no value.
        """
        parent = "".join([path[0] for path in self._split_path(path)[:-1]])
        elem = self._get_or_create_element(parent)
        tag, attribs = self._parse_node(self._split_path(path)[-1][0])
        new = _to_json(attribs, value)
        return _add_element(elem, tag, new)

    def add_element(self, path: str, value: str | None = None) -> JsonType:
        """Adds an element if it not already exists.

        Otherwise it appends the string to the already existing element.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        elem = self._get_or_create_element(path)
        text = elem.get("#text", "")
        elem["#text"] = f"{text}{value}"
        return elem

    def enter_path(self, path: str, value: str | None = None) -> None:
        """Enter a node and create elements in the path if they do not already exist.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        elem = self._get_or_create_element(path)
        if value is not None:
            elem["#text"] = value
        self.prev_roots.append(self.root)
        self.root = elem

    def open_path(self, path: str, value: str | None = None) -> None:
        """Enter a node and create elements in the path if they do not already exist.

        Always creates the last node.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        elem = self.create_element(path)
        self.prev_roots.append(self.root)
        self.root = elem

    def leave_path(self) -> None:
        """Set the current root object to the previous one."""
        self.root = self.prev_roots.pop()

    def delete_element(self, path: str) -> None:
        """Delete an element.

        :param path: Path of the element.
        """
        parent = "".join([path[0] for path in self._split_path(path)[:-1]])
        elem = self._get_element(parent)
        elem.pop(self._split_path(path)[-1][2])

    def replace_element(self, path: str, value: str | None = None) -> None:
        """Replace an element.

        :param path: Path of the element.
        :param value: Value of the replaced element or None if it has no value.
        """
        parent = "".join([path[0] for path in self._split_path(path)[:-1]])
        elem = self._get_element(parent)
        if value is not None:
            elem["#text"] = value
        else:
            elem.pop("#text", None)

    def generate_output(self) -> str:
        """Generate output in specified format."""
        tree = self.tree
        if self.root_name is not None:
            tree = tree[self.root_name] = tree
        return json.dumps(tree, indent=4)
