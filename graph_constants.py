from pydantic import BaseModel, Field
from enum import Enum
from icecream import ic


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
    SENSITIVITY = "sensitivity"
    ACTION = "action"
    ACTION_UNPROCESSED = "action_unprocessed"
    SENSITIVITY_ACTION = "sensitivity_action"

class HomeEnum(Enum):
    NAME = "id"

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
        self.node_type: DeviceEnum | HomeEnum = node_type


class GraphTree:
    def __init__(self, root: Node):
        self.root = root

    def get_root(self):
        return self.root

    def add_child(self, parent_node: Node | None, child_node: Node):
        if parent_node is not None:
            # check parent node is redundant?
            if parent_node.id not in self.get_parent_id(node=child_node):
                child_node.parent.append(parent_node)
                child_node = self.append_id_parent(
                    node=child_node
                )  # change id by adding parent id

            for _parent_node in child_node.parent:
                # check is id of children is redundant?
                if child_node.id not in self.get_child_id(node=_parent_node):
                    _parent_node.children.append(child_node)
        return child_node

    def add_mul_child(self, parent_node: Node, child_node: list[Node]):
        # add multiple children
        for _child in child_node:
            _ = self.add_child(parent_node=parent_node, child_node=_child)

        return child_node

    def add_child_mul_parent(self, parent_node: list[Node], child_node=Node):

        # for add child node with multiple parent
        for _parent in parent_node:
            _ = self.add_child(parent_node=_parent, child_node=child_node)

        return child_node

    def get_child_id(self, node: Node):
        id_list = list([x.id for x in node.children])
        return id_list

    def get_parent_id(self, node: Node):
        id_list = list([x.id for x in node.parent])
        return id_list

    def append_id_parent(self, node: Node):
        if node.parent is not None:
            parent_id = ""

            for parent in node.parent:
                parent_id += parent.id

            node.id = f"{parent_id}_{node.id}".replace(" ", "_")
        return node

    def max_depth(self, node: Node) -> int:
        if node is None:
            return 0
        elif len(node.children) == 0:
            return 1
        else:
            return 1 + max(self.max_depth(child) for child in node.children)

    def gen_data_visual(
        self,
        top_x: int,
        top_y: int,
        # screen_width: int,
        # screen_height: int,
        width_slot: int,
        height_slot: int,
        start_node: Node = None,
        data_visual_list: list = [],
    ):

        # ic(top_x, top_y, width_slot, height_slot)

        if start_node is not None:

            data_visual_list.append(
                self.create_node_visual(
                    id=start_node.id,
                    label=start_node.label,
                    x=top_x + int(width_slot / 2),
                    y=top_y + int(height_slot / 2),
                )
            )  # append own node

            number_child = len(start_node.children)
            if number_child > 0:  # go to children node
                # calculate the height slot of each child node
                new_height_slot = height_slot / number_child
                new_width_slot = width_slot

                for index, child in enumerate(start_node.children):
                    # check the same parent

                    
                    
                    child_dict = self.gen_data_visual(
                        top_x=top_x + new_width_slot,
                        top_y=top_y + (index * new_height_slot),
                        width_slot=new_width_slot,
                        height_slot=new_height_slot,
                        start_node=child,
                        data_visual_list=data_visual_list,
                    )

                    if child_dict is not None:
                        data_visual_list.append(child_dict)

            if start_node.id == self.root.id:
                return data_visual_list

    # def

    def create_node_visual(self, id: str, label: str, x: int, y: int):
        return {
            "data": {"id": id, "label": label},
            "position": {"x": x, "y": y},
        }

    def create_relation_visual(self, source: str, target: str):
        return {
            "data": {"source": source, "target": target},
        }

    def print_tree(self, show_id=False, show_level=False):
        self._print_tree_recursive(
            node=self.root, show_id=show_id, show_level=show_level
        )

    def _print_tree_recursive(
        self, node: Node, level=0, show_id=False, show_level=False
    ):
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

class DeviceTree:
    home_id: str
    home_label: str
    devices: list[Device] = []

    def merge_device_tree(self) -> GraphTree:
        # Create Home Node 
        home_node = Node(id="H_0", label="My home",parent=[], node_type=HomeEnum.ID)
        
        # Create Device Node for each device
        
        
        return None
