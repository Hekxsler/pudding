"""Module defining xml writer class."""

from lxml import etree

from .writer import Writer, Node


class Xml(Writer):
    """Writer class for xml output."""

    def __init__(self, root_name: str = "xml") -> None:
        """Init for Xml writer class."""
        self.prev_roots: list[Node] = []
        self.root = Node(root_name)
        super().__init__(root_name)

    def _get_element(self, path: str) -> Node:
        """Get first Node at given path.

        :param path: Path from root element.
        :returns: Node at the given path.
        :raises ValueError: If no element is found.
        """
        elem = self.root.find(path)
        if elem is None:
            raise ValueError(f"Node at path {path} does not exist")
        return elem

    def _get_or_create_element(self, path: str, root: Node) -> Node:
        """Get first Node at given path or create it if it does not exist.

        :param xpath: Path from root element.
        :param root: Node to start from.
        :returns: Node at the given path.
        """
        if path in ["", "."]:
            return root
        sub_paths = self._split_path(path)
        if len(sub_paths) > 1:
            root = self._get_or_create_element(sub_paths[0][0], root)
            for sub_path in sub_paths[1:]:
                root = self._get_or_create_element(sub_path[0].lstrip("/"), root)
            return root
        elem = self.root.find(path)
        if elem is not None:
            return elem
        name, attribs = self._parse_node(path)
        return self.root.add_child(name, attribs)

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
        else:
            parent_path = "".join(path[0] for path in self._split_path(path)[:-1])
            parent = self._get_or_create_element(parent_path, self.root)
            name, attribs = self._parse_node(self._split_path(path)[-1][0])
            new = parent.add_child(name, attribs)
        new.text = value
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

    def serialize_node(self, node: Node) -> etree.Element:
        root = etree.Element(node.name, node.attribs)
        root.text = node.text
        for child in node.children:
            root.append(self.serialize_node(child))
        return root

    def generate_output(self) -> str:
        """Generate output in specified format."""
        if self.root_name is not None:
            self.root.name = self.root_name
        tree = self.serialize_node(self.root)
        return etree.tostring(tree, pretty_print=True, encoding=str)
