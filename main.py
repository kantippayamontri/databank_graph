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
from dash import Dash, html, Input, Output, callback, no_update
import dash_cytoscape as cyto

app = Dash(__name__)

screen_width = 2000
screen_heigth = 500

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
screen_width_ratio = screen_height_ratio = 1.0

if devices is not None:

    each_device_height = int(
        (screen_height_ratio / len(devices)) * device_screen_height
    )
    each_device_width = screen_width_ratio * device_screen_width

    # Create Home Tree
    home_tree = HomeTree(home_id="h_0", home_label="Home", devices=devices)

    ic(home_tree.get_root().id)
    ic(home_tree.max_depth())
    home_tree.print_tree()

device_graph_list = home_tree.gen_data_visual_home(
    start_node=home_tree.get_root(),
    top_x=0,
    top_y=0,
    screen_width=device_screen_width,
    screen_height=device_screen_height,
)

ic(device_graph_list)

# prepare node for service
service_graph_list = []
if services is not None:
    each_service_height = int((screen_height_ratio / len(services)) * service_screen_heigth)
    each_service_width = screen_width_ratio * service_screen_width


app.layout = html.Div(
    [
        html.P(id="tapNode"),
        html.P(id="tapEdge"),
        html.P(id="mouseOverNode"),
        html.P(id="mouseOverEdge"),
        cyto.Cytoscape(
            id="databank-graph",
            layout={"name": "preset"},
            style={
                "width": str(screen_width) + "px",
                "height": str(screen_heigth) + "px",
            },
            elements=device_graph_list,
            stylesheet=[
                # Group selectora
                {
                    "selector": "edge",
                    "style": {
                        "curve-style": "bezier"  # must define to custom relation edge
                    },
                },
                {
                    "selector": ".home",
                    "style": {"background-color": "#3498db", "content": "data(label)"},
                },
                # Device node
                {
                    "selector": ".device_normal",
                    "style": {"background-color": "#148f77", "content": "data(label)"},
                },
                {
                    "selector": ".device_special",
                    "style": {"background-color": "#f39c12", "content": "data(label)"},
                },
                # Device relation
                {
                    "selector": '[id *= "relation_"]',
                    "style": {
                        "line-color": "black",
                        "target-arrow-color": "black",
                        "target-arrow-shape": "triangle",
                    },
                },
            ],
        ),
    ]
)


# Create callback when click node
@callback(Output("tapNode", "children"), Input("databank-graph", "tapNodeData"))
def displayTapNodeData(data):
    if data:
        return f"Tap node data: {data['label']}"
    else:
        return "Tap node data: None"


# Create callback when click edge
@callback(Output("tapEdge", "children"), Input("databank-graph", "tapEdgeData"))
def displayTapEdgeData(data):
    if data:
        return f"Tap edge data: {data['id']}"
    else:
        return "Tap edge data: None"


# Create callback when mouse over node
@callback(
    Output("mouseOverNode", "children"), Input("databank-graph", "mouseoverNodeData")
)
def displayMouseOverNodeData(data):
    if data:
        return f"Mouse over node data: {data['label']}"
    else:
        return "Mouse over node data: None"


# Create callback when mouse over edge
@callback(
    Output("mouseOverEdge", "children"), Input("databank-graph", "mouseoverEdgeData")
)
def displayMouseOverEdgeData(data):
    if data:
        return f"Mouse over edge data: {data['id']}"
    else:
        return "Mouse over edge data: None"


if __name__ == "__main__":
    app.run(debug=True)  # type: ignore
