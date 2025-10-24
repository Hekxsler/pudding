"""Module defining base writer class."""

from pathlib import Path
from typing import Any

from ..node import Node


class Writer:
    """Base writer class.

    :var attrib_re: Regex for node attributes.
    :var node_re: Regex for a node path.
    """

    def __init__(self, root_name: str = "root") -> None:
        """Init for writer class."""
        self.root_name = root_name

    def add_attribute(self, path: str, name: str, value: str) -> None:
        """Add an attribute to an element.

        :param path: Path of the element.
        :param name: Name of the attribute.
        :param value: Value of the attribute.
        """
        raise NotImplementedError

    def create_element(self, path: str, value: str | None = None) -> Any:
        """Add an element to the current node.

        :param path: Path of the element.
        :param value: Value of the element or None if it has no value.
        :returns: The created element.
        """
        raise NotImplementedError

    def add_element(self, path: str, value: str | None = None) -> Any:
        """Add an element if it not already exists.

        Otherwise it appends the string to the already existing element.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        :returns: The created element.
        """
        raise NotImplementedError

    def enter_path(self, path: str, value: str | None = None) -> None:
        """Enter a node and create elements in the path if they do not already exist.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        raise NotImplementedError

    def open_path(self, path: str, value: str | None = None) -> None:
        """Enter a node and create elements in the path if they do not already exist.

        Always creates the last node.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        raise NotImplementedError

    def leave_path(self) -> None:
        """Leave the previously entered path."""
        raise NotImplementedError

    def delete_element(self, path: str) -> None:
        """Delete an element.

        :param path: Path of the element.
        """
        raise NotImplementedError

    def replace_element(self, path: str, value: str | None = None) -> None:
        """Replace an element.

        :param path: Path of the element.
        :param value: Value of the replaced element or None if it has no value.
        """
        raise NotImplementedError

    def generate_output(self) -> str:
        """Generate output in specified format."""
        raise NotImplementedError

    def print_output(self) -> None:
        """Print output to stdout."""
        print(self.generate_output())

    def write_to(self, file_path: Path, encoding: str = "utf-8") -> None:
        """Write generated output to file.

        :param file_path: Path of the file to write to.
        """
        with open(file_path, "w", encoding=encoding) as f:
            f.write(self.generate_output())


class BufferedWriter(Writer):
    """Base writer class for buffered output.

    :var attrib_re: Regex for node attributes.
    :var node_re: Regex for a node path.
    """

    def __init__(self, root_name: str = "root") -> None:
        super().__init__(root_name)
        self.prev_roots: list[Node] = []
        self.root = Node(root_name)

    def _get_element(self, path: str) -> Node:
        """Get first Node at given path.

        :param path: Path from root element.
        :returns: Node at the given path.
        :raises ValueError: If no element is found.
        """
        elem = self.root.find(path)
        if elem is None:
            raise ValueError(f"Node at path {repr(path)} does not exist")
        return elem

    def _get_or_create_element(self, path: str, root: Node) -> Node:
        """Get first Node at given path or create it if it does not exist.

        :param xpath: Path from root element.
        :param root: Node to start from.
        :returns: Node at the given path.
        """
        if path in ["", "."]:
            return root
        sub_paths = Node.split_path(path)
        if len(sub_paths) > 1:
            root = self._get_or_create_element(sub_paths[0][0], root)
            for sub_path in sub_paths[1:]:
                root = self._get_or_create_element(sub_path[0].lstrip("/"), root)
            return root
        elem = self.root.find(path)
        if elem is not None:
            return elem
        new = Node.from_path(path)
        self.root.add_child(new)
        return new

    def add_attribute(self, path: str, name: str, value: str) -> None:
        """Add an attribute to an element.

        :param path: Path of the element.
        :param name: Name of the attribute.
        :param value: Value of the attribute.
        """
        elem = self._get_element(path)
        elem.set(name, value)

    def create_element(self, path: str, value: str | None = None) -> Node:
        """Add an element and always create the last element in the path.

        :param path: Path of the element.
        :param value: Value of the element or None if it has no value.
        :returns: The created SubElement.
        """
        elem = self.root.find(path)
        if elem is None:
            new = self._get_or_create_element(path, self.root)
            new.text = value
            return new
        paths = Node.split_path(path)
        if len(paths) == 0:
            raise ValueError(f"Invalid path {repr(path)}.")
        if len(paths) == 1:
            parent = self.root
            child_node = paths[0][0]
        else:
            *parent_paths, child_path = paths
            parent_path = "".join((path[0] for path in parent_paths))
            parent = self._get_or_create_element(parent_path, self.root)
            child_node = child_path[0]
        new = Node.from_path(child_node, value)
        parent.add_child(new)
        return new

    def add_element(self, path: str, value: str | None = None) -> Node:
        """Add an element if it not already exists.

        Otherwise it appends the string to the already existing element.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        :returns: The added/modified SubElement.
        """
        elem = self._get_or_create_element(path, self.root)
        text = elem.text or ""
        if value is not None:
            elem.text = f"{text}{value}"
        return elem

    def enter_path(self, path: str, value: str | None = None) -> None:
        """Enter a node and create elements in the path if they do not already exist.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        elem = self._get_or_create_element(path, self.root)
        elem.text = value
        self.prev_roots.append(self.root)
        self.root = elem

    def open_path(self, path: str, value: str | None = None) -> None:
        """Enter a node and create elements in the path if they do not already exist.

        Always creates the last node.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        """
        elem = self.create_element(path, value)
        self.prev_roots.append(self.root)
        self.root = elem

    def leave_path(self) -> None:
        """Set the current root object to the previous one."""
        self.root = self.prev_roots.pop()

    def delete_element(self, path: str) -> None:
        """Delete an element.

        :param path: Path of the element.
        """
        elem = self._get_element(path)
        del elem

    def replace_element(self, path: str, value: str | None = None) -> None:
        """Replace an element.

        :param path: Path of the element.
        :param value: Value of the replaced element or None if it has no value.
        """
        elem = self._get_element(path)
        elem.text = value
