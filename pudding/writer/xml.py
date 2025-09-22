"""Module defining xml writer class."""

from lxml.etree import Element, ElementTree, SubElement, tostring

from .writer import Writer


class Xml(Writer):
    """Writer class for xml output."""

    prev_roots: list[Element] = []
    root_name = "xml"

    def __init__(self) -> None:
        self.root = Element(self.root_name)
        self.tree = ElementTree(self.root)
        super().__init__()

    def _find(self, elem: Element, path: str) -> Element | None:
        """Find first matching element at path.
        
        :param elem: Element to search from.
        :param path: Path to another element.
        :returns: The first element found or none if it does not exist.
        """
        xpath = self._to_xpath(path)
        # Workaround for lxml.find not working with xpath attributes
        try:
            return elem.xpath(xpath)[0]
        except IndexError:
            return None

    def _get_element(self, path: str) -> Element:
        """Get first Element at given path.

        :param path: Path from root element.
        :returns: Element at the given path.
        :raises ValueError: If no element is found.
        """
        elem = self._find(self.root, path)
        if elem is None:
            raise ValueError(f"Element at path {path} does not exist")
        return elem

    def _get_or_create_element(self, path: str, root: Element) -> Element:
        """Get first Element at given path or create it if it does not exist.

        :param xpath: Path from root element.
        :param root: Element to start from.
        :returns: Element at the given path.
        """
        if path in ["", "."]:
            return root
        sub_paths = self._split_path(path)
        if len(sub_paths) > 1:
            root = self._get_or_create_element(sub_paths[0][0], root)
            for sub_path in sub_paths[1:]:
                root = self._get_or_create_element(sub_path[0].lstrip("/"), root)
            return root
        elem = self._find(root, path)
        if elem is not None:
            return elem
        name, attribs = self._parse_node(path)
        return SubElement(root, name, attribs)

    def _to_xpath(self, path: str) -> str:
        """Convert path to an xpath."""
        for node in super().node_re.findall(path):
            tag = node[2].replace(" ", "-")
            if not node[3]:
                path = path.replace(node[0], f"{node[1]}{tag}[not(@*)]")
                # match only nodes without attributes
                continue
            attributes = super().attrib_re.findall(node[3])
            if len(attributes) == 1:
                attribs = f'[@{attributes[0][1]}="{attributes[0][2]}" and count(@*)=1]'
            else:
                attribs = f'[@{attributes[0][1]}="{attributes[0][2]}"'
                for attribute in attributes:
                    value = attribute[2].replace('"', '\\"')
                    attribs += f' and @{attribute[1]}="{value}"'
                attribs += f" and count(@*)={len(attributes)}]"
            path = path.replace(node[0], f"{node[1]}{tag}{attribs}")
        return path

    def add_attribute(self, path: str, name: str, value: str) -> None:
        """Add an attribute to an element.

        :param path: Path of the element.
        :param name: Name of the attribute.
        :param value: Value of the attribute."""
        elem = self._get_element(path)
        elem.set(name, value)

    def create_element(self, path: str, value: str | None = None) -> Element:
        """Add an element at the given path and always create the last element in the path.

        :param path: Path of the element.
        :param value: Value of the element or None if it has no value.
        :returns: The created SubElement.
        """
        elem = self._find(self.root, path)
        if elem is None:
            new = self._get_or_create_element(path, self.root)
        else:
            parent = elem.getparent()
            if parent is None:
                parent = self.tree.getroot()
            node = self._split_path(path)[-1][0]
            name, attribs = self._parse_node(node)
            new = SubElement(parent, name, attribs)
        new.text = value
        return new

    def add_element(self, path: str, value: str | None = None) -> Element:
        """Adds an element if it not already exists. Otherwise it appends the string
        to the already existing element.

        :param path: Path to the element.
        :param value: Value of the element or None if it has no value.
        :returns: The added/modified SubElement.
        """
        elem = self._get_or_create_element(path, self.root)
        text = elem.text
        if text is None:
            text = ""
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
        """Enter a node and create elements in the path if they do not already exist,
        but alway create the last node in the path.

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
        parent = elem.getparent()
        if parent is None:
            raise ValueError("Cannot delete root element.")
        parent.remove(elem)

    def replace_element(self, path: str, value: str | None = None) -> None:
        """Replace an element.

        :param path: Path of the element.
        :param value: Value of the replaced element or None if it has no value.
        """
        self.delete_element(path)
        self.add_element(path, value)

    def generate_output(self) -> str:
        """Generate output in specified format."""
        root = self.tree.getroot()
        if root is None:
            raise ValueError("No root element set.")
        root.tag = self.root_name
        return tostring(root, pretty_print=True).decode()
