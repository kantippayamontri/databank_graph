from icecream import ic
from graph_constants import *
from mock_data import data


# code to generate graph
def create_elements(
    _data: dict | None,
) -> tuple[list[Device] | None, list[Service] | None]:
    data: dict | None = _data
    # check device
    if not data:
        return None, None

    devices = []
    if "devices" in data.keys():
        for device_id in data["devices"].keys():
            if "raw_data" not in data["devices"][device_id].keys():
                data["devices"][device_id]["raw_data"] = None
            device = Device(**data["devices"][device_id], id=device_id)
            devices.append(device)
    else:
        ic(f"Devices not found.")

    services = []
    if "services" in data.keys():
        ic(f"Services found.")
    else:
        ic(f"Services not found.")

    return devices, services


# def create_device_graph(
#     device: Device, start_h:int,slot_h:int, hslot_h:int
# ) -> list[Node | Relation] | None:
#     ic(device.model_dump_json())
#     device_node_relation_list: list[Node | Relation] = []
#     # Create node device node
#     device_node = Node(
#         data=Data(id="d_" + device.id, label=device.name), position=Position(x=0, y=start_h)
#     )
#     device_node_relation_list.append(device_node)

#     # Create unprocessed node
#     for un_index ,_un in enumerate(device.unprocessed_data):
#         un_node = Node(
#             data=Data(id=f"un_{device.id}_{un_index}", label=_un),
#             position=Position(x=50, y=start_h)
#         )

#         device_node_relation_list.append(un_node)

#         # Create relation device_node and unprocessed
#         relation_node = Relation(
#             data=RelationData(
#                 source=device_node.data.id,
#                 target=un_node.data.id
#             )
#         )

#         device_node_relation_list.append(relation_node)

#         if device.raw_data is not None: # found raw data
#             if _un in device.raw_data.keys(): # unprocessed data has details
#                 #create action node
#                 action_node = Node(
#                     data=Data(
#                        id=f"action_{device.id}_{un_index}",
#                        label=device.raw_data[_un]["action"]
#                         ),
#                     position=Position(
#                         x=100,
#                         y=start_h,
#                     )
#                 )

#                 device_node_relation_list.append(action_node)

#         start_h += hslot_h


#     return device_node_relation_list


def create_device_tree(device: Device | None):
    # ic(device.model_dump())
    if device is None:
        return None

    # Create Tree and add device node
    tree = GraphTree(
        root=Node(
            id=str("d_" + device.id).replace(" ", "_"),
            label=device.name,
            node_type=DeviceEnum.NAME,
        )
    )
    root = tree.get_root()
    # Create Device type Node
    if device.type is not None:
        device_type_node = Node(
            id="dt_" + device.type, label=device.type, node_type=DeviceEnum.TYPE
        )
        current_node = tree.add_child(parent_node=root, child_node=device_type_node)

    device_type_node_temp = current_node  # for separate unprocessed data branch

    # Create Device unprocessed Node
    if device.unprocessed_data is not None:
        for _un in device.unprocessed_data:
            un_processed_node = Node(
                id="un_" + _un, label=_un, node_type=DeviceEnum.UNPROCESSED_DATA
            )
            current_node = tree.add_child(
                parent_node=device_type_node_temp, child_node=un_processed_node
            )

            # Create raw data
            if device.raw_data is None:
                continue

            if _un in device.raw_data.keys():  # found raw data

                # Create category -> sensitivity node
                sensitivity = device_category_mapping[
                    (
                        device.raw_data[_un]["action"],
                        device.raw_data[_un]["frequency"],
                        device.raw_data[_un]["sensitivity"],
                    )
                ]
                sensitivity_node = Node(
                    id="sen_" + sensitivity,
                    label=sensitivity,
                    node_type=DeviceEnum.SENSITIVITY,
                )
                current_node = tree.add_child(
                    parent_node=current_node, child_node=sensitivity_node
                )

                # Create action node
                action = device.raw_data[_un]["action"]
                action_node = Node(
                    id="at_" + action, label=action, node_type=DeviceEnum.ACTION
                )

                # Create action unprocessed node #TODO: orange node
                action_unprocessed = action + "_" + _un
                action_unprocessed_node = Node(
                    id="atun_" + action_unprocessed,
                    label=action_unprocessed.replace("_", "_"),
                    node_type=DeviceEnum.ACTION_UNPROCESSED,
                )

                current_node: list[Node] = tree.add_mul_child(
                    parent_node=current_node,
                    child_node=[action_node, action_unprocessed_node],
                )  # return multiple child node

                # Create sensitivity action
                sensitivity_action = sensitivity + "_" + action
                sensitivity_action_node = Node(
                    id="senat_" + sensitivity_action,
                    label=sensitivity_action,
                    node_type=DeviceEnum.SENSITIVITY_ACTION,
                )

                current_node = tree.add_child_mul_parent(
                    parent_node=current_node, child_node=sensitivity_action_node
                )

    # print(tree._print_tree_recursive(node=current_node_temp))

    # if current_node is not None:
    #     if device.unprocessed_data:
    #         for _un in device.unprocessed_data:
    #             unprocess_node =

    return tree


# TODO: making graph
from dash import Dash, html
import dash_cytoscape as cyto

# import tkinter as tk

app = Dash(__name__)

# root = tk.Tk()
# screen_width = root.winfo_screenwidth()
# screen_heigth = root.winfo_screenheight()

screen_width = 2000
screen_heigth = 2000

device_screen_width = service_screen_width = int(screen_width / 2)
device_screen_height = service_screen_heigth = screen_heigth

devices, services = create_elements(data)
if devices:
    ic(f"--- Devices found ---")
    # for device in devices:
    #     ic(device.model_dump_json())

if services:
    ic(f"--- Services found ---")
    # for service in services:
    #     ic(service.model_dump_json())

# prepare node for device
device_graph_list = []
if devices is not None:

    screen_width_ratio = screen_height_ratio = 1.0
    each_device_height = int((screen_height_ratio / len(devices)) * device_screen_height)
    each_device_width = screen_width_ratio * device_screen_width

    device_tree_list = []
    for index, device in enumerate(devices):
        # TODO: create device tree
        device_tree = create_device_tree(device=device)
        ic(device_tree.max_depth(node=device_tree.root))
        device_tree_list.append(device_tree)
    
    for _device_tree in device_tree_list:
        ...

        # device_width_slot = int(each_device_width / device_tree.max_depth(node=device_tree.root))
        # device_height_slot = int(each_device_height)

        # device_tree.print_tree(show_id=False, show_level=True)
        # device_graph_list = device_tree.gen_data_visual(
        #     start_node=device_tree.root,
        #     top_x=0,
        #     top_y=(index * each_device_height),
        #     width_slot = device_width_slot,
        #     height_slot = device_height_slot,
        # )

# ic(screen_width, screen_heigth)

# device_graph_list = [
#     {"data": {"id": "one", "label": "Node 1"}, "position": {"x": 75, "y": 75}},
#     {"data": {"id": "two", "label": "Node 2"}, "position": {"x": 200, "y": 200}},
#     {"data": {"source": "one", "target": "two"}},
# ]

ic(device_graph_list)

app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="databank-graph",
            layout={"name": "preset"},
            style={
                "width": str(screen_width) + "px",
                "height": str(screen_heigth) + "px",
            },
            elements=device_graph_list,
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)  # type: ignore
