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
    each_device_height = int(
        (screen_height_ratio / len(devices)) * device_screen_height
    )
    each_device_width = screen_width_ratio * device_screen_width

    # Create Home Tree
    home_tree = HomeTree(home_id="h_0", home_label="Home", devices=devices)

    ic(home_tree.get_root().id)
    ic(home_tree.max_depth())
    home_tree.print_tree()

    # device_tree_list = []
    # device_tree_list = home_tree.gen_data_visual(
    #     top_x=0,
    #     top_y=0,
    #     width_slot=0,
    #     height_slot=0,
    # )

    # device_tree_list = []
    # for index, device in enumerate(devices):
    #     # TODO: create device tree
    #     device_tree = create_device_tree(device=device)
    #     ic(device_tree.max_depth(node=device_tree.root))
    #     device_tree_list.append(device_tree)

    # for _device_tree in device_tree_list:
    #     ...

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

device_graph_list = home_tree.gen_data_visual(
    start_node=home_tree.get_root(),    
    top_x=0,
    top_y=0,
    width_slot=each_device_width,
    height_slot=each_device_height,
)

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
