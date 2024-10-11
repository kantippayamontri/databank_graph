from icecream import ic
from graph_constants import *
from mock_data import data
from graph_utils import create_elements, create_home_tree, create_company_tree

# TODO: making graph
from dash import Dash, html, Input, Output, callback, no_update
import dash_cytoscape as cyto


#def defind screen size 
screen_width = 2000
screen_heigth = 500

#def devide screen size for device and service
device_screen_width = service_screen_width = int(screen_width / 2)
device_screen_height = service_screen_heigth = screen_heigth

devices, services = create_elements(data) # get devices and services from data

home_tree = create_home_tree(devices=devices) # make tree for device

#gen grapg for visual for device
device_graph_list = home_tree.gen_data_visual_home(
   top_x=0,
   top_y=0,
   screen_width=device_screen_width,
   screen_height=device_screen_height,
   show_home_node=False  #start from device node
)

# ic(device_graph_list)

# prepare node for service
service_graph_list = []
if len(services):
    each_service_height = int(
        (1 / len(services)) * service_screen_heigth
    )
    each_service_width = 1 * service_screen_width

    companyTree = create_company_tree(services=services)


# Dash App
app = Dash(__name__)

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
            elements=device_graph_list + service_graph_list,
            stylesheet=[
                # Group selector
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
