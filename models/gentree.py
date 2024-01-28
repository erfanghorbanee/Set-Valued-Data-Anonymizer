from typing import Dict, List, Optional


class GenTree(object):

    """
    Class for Generalization hierarchies (Taxonomy Tree).
    Store tree node in instances.
    self.value: node value
    self.level: tree level (top is 0)
    self.leaf_num: number of leaf node covered
    self.parent: ancestor node list
    self.child: direct successor node list
    self.cover: all nodes covered by current node
    """

    def __init__(
        self,
        value: Optional[str] = None,
        parent: Optional["GenTree"] = None,
        isleaf: bool = False,
    ) -> None:
        self.value = value if value is not None else ""
        self.level = parent.level + 1 if parent is not None else 0
        self.leaf_num = 0
        self.parent = parent.parent[:] if parent is not None else []
        self.child: List["GenTree"] = []
        self.cover: Dict[str, "GenTree"] = (
            {self.value: self} if value is not None else {}
        )

        if parent is not None:
            self.parent.insert(0, parent)
            parent.child.append(self)
            for t in self.parent:
                t.cover[self.value] = self
                if isleaf:
                    t.leaf_num += 1

    def node(self, value: str) -> Optional["GenTree"]:
        return self.cover.get(value, None)

    def __len__(self) -> int:
        """
        return number of leaf node covered by current node
        """
        return self.leaf_num

    def add_node(self, value: str, isleaf: bool = False) -> "GenTree":
        if value not in self.cover:
            new_node = GenTree(value, self, isleaf)
            self.cover[value] = new_node
            return new_node
        return self.cover[value]

    def __repr__(self) -> str:
        return f"Value: {self.value}, Level: {self.level}, Leaf Num: {self.leaf_num}"
