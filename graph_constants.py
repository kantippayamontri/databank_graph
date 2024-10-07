from pydantic import BaseModel, Field
from enum import Enum


class Device(BaseModel):
    id: str
    name: str = Field(alias="device_name")
    type: str = Field(alias="device_type")
    unprocessed_data: list[str] = Field(alias="device_unprocessed")
    raw_data: dict[str, dict[str, str]] | None = Field(alias="raw_data")


class DeviceEnum(Enum):
    NAME = "name"
    TYPE = "type"
    UNPROCESSED_DATA = "unprocessed_data"
    CATEGORY = "category"



device_category_mapping = {
    ("Average", "Daily", "Low"): "Private",
    ("Transfer", "Daily", "Low"): "Private",
    ("Anonymise", "Daily", "Low"): "Private",
    ("Average", "Daily", "High"): "Protected",
    ("Transfer", "Daily", "High"): "Protected",
    ("Anonymise", "Daily", "High"): "Protected",
    ("Average", "Daily", "Medium"): "Secert",
    ("Transfer", "Daily", "Medium"): "Secert",
    ("Anonymise", "Daily", "Medium"): "Secert",
    ("Average", "Weekly", "Low"): "Confidential",
    ("Transfer", "Weekly", "Low"): "Confidential",
    ("Anonymise", "Weekly", "Low"): "Confidential",
    ("Average", "Weekly", "High"): "Restricted",
    ("Transfer", "Weekly", "High"): "Restricted",
    ("Anonymise", "Weekly", "High"): "Restricted",
    ("Average", "Monthly", "Low"): "Private",
    ("Transfer", "Monthly", "Low"): "Private",
    ("Anonymise", "Monthly", "Low"): "Private",
    ("Average", "Monthly", "High"): "Protected",
    ("Transfer", "Monthly", "High"): "Protected",
    ("Anonymise", "Monthly", "High"): "Protected",
    ("Average", "Monthly", "Medium"): "Protected",
    ("Transfer", "Monthly", "Medium"): "Protected",
    ("Anonymise", "Monthly", "Medium"): "Protected",
    ("Average", "Yearly", "Low"): "Confidential",
    ("Transfer", "Yearly", "Low"): "Confidential",
    ("Anonymise", "Yearly", "Low"): "Confidential",
    ("Average", "Yearly", "High"): "Restricted",
    ("Transfer", "Yearly", "High"): "Secret",
    ("Average", "Yearly", "High"): "Restricted",
    ("Upload", "Yearly", "Medium"): "Protected",
}

class Service(BaseModel): ...

class Data(BaseModel):
    id: str
    label: str

class Position(BaseModel):
    x: int
    y: int

# class RelationData(BaseModel):
#     source: str
#     target: str

class GraphNode(BaseModel):
    data: Data
    position: Position

# class Relation(BaseModel):
#     data: RelationData | None

class Node:
    def __init__(self, id: str, label: str, node_type: DeviceEnum):
        self.id: str = id
        self.label: str = label
        self.children: list[Node] | None = []
        self.parent: list[Node] = []
        self.node_type: DeviceEnum = node_type 

class GraphTree:
    def __init__(self, root: Node):
        self.root = root

    def get_root(self):
        return self.root

    def add_child(self, parent_node: Node | None, child_node: Node):
        if parent_node is not None:
            child_node.parent.append(parent_node)
            child_node = self.append_id_parent(
                node=child_node
            )  # change id by adding parent id
            for _parent_node in child_node.parent:
                _parent_node.children.append(child_node)
        return child_node

    def append_id_parent(self, node: Node):
        if node.parent is not None:
            parent_id = ""

            for parent in node.parent:
                parent_id += parent.id

            node.id = f"{parent_id}_{node.id}".replace(" ", "_")
        return node

    def print_tree(self, show_id=False, show_level=False):
        self._print_tree_recursive(
            node=self.root, show_id=show_id, show_level=show_level
        )

    def _print_tree_recursive(self, node, level=0, show_id=False, show_level=False):
        show_string = str(node.label)

        if show_level:
            show_string = f"[{level}] " + show_string

        show_string = "  " * level + show_string

        if show_id:
            show_string = show_string + f" ({str(node.id)})"

        print(show_string)

        for child in node.children:
            self._print_tree_recursive(
                node=child, level=level + 1, show_id=show_id, show_level=show_level
            )