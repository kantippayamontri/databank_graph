data = {
    "devices": {
        "0": {
            "device_name": "Gauge",
            "device_type": "Security Camera",
            "device_unprocessed": ["Footage"],
        },
        "1": {
            "device_name": "smart meter",
            "device_type": "Security Camera",
            "device_unprocessed": ["Footage", "activity"],
            "raw_data": {
                "Footage": {
                    "action": "Average",
                    "frequency": "Daily",
                    "sensitivity": "Low",
                }
            },
        },
    },
    "services": {
        "0": {
            "cate_service": {
                "1": {
                    "Footage": {
                        "action": "View Data",
                        "category": "Low",
                        "frequency": "Daily",
                    }
                }
            },
            "service_name": "Meta",
            "service_type": "Advertising Company",
        },
        "1": {"service_name": "Meta_(1)", "service_type": "Tech Company"},
    },
}

from icecream import ic
from graph_constants import (
    Device,
    Service,
    Data,
    Position,
    RelationData,
    Node,
    Relation,
)
import random


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
            device = Device(**data["devices"][device_id])
            devices.append(device)
    else:
        ic(f"Devices not found.")

    services = []
    if "services" in data.keys():
        ic(f"Services found.")
    else:
        ic(f"Services not found.")

    return devices, services


def create_device_graph(device: Device) -> list[Node | Relation] | None:
    ic(device.model_dump_json())
    # Create node device node
    device_node = Node(data=Data(id="", label=""),
                       position=Position(x=0, y=0))
    return None


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
device_graph_list: list[Node] | None = []
if devices is not None:
    for device in devices:
        device_node = create_device_graph(device)
        if device_node is not None:
            for ele in device_node:
                ic(ele.model_dump_json())
            exit()  # FIXME: remove this


# TODO: making graph
# from dash import Dash, html
# import dash_cytoscape as cyto

# app = Dash(__name__)

# devices_graph = list([ create_node() for device in devices])

# app.layout = html.Div(
#     [
#         cyto.Cytoscape(
#             id="databank-graph",
#             layout={'name': "preset"},
#             style={'width': "100%", "height": "100%"},
#             elements=[

#                 ],
#         )
#     ]
# )
# # create device part
