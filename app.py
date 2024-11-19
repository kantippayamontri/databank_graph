from icecream import ic
from graph_constants import *
# from mock_data import data
from graph_utils import create_elements, create_home_tree, create_company_tree, create_relation_service_device
from graph_style import stylesheet   


# TODO: making graph
from dash import dcc, Dash, html, Input, Output, callback, no_update
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

data= {'data':{'devices':{},'services':{}},'screenWidth':1920}
trigger_web_hook = 0
device_graph_list = []
service_graph_list = []
relation = []
# Dash App
server = Flask(__name__)
app = Dash(__name__, server=server)
CORS(server)

@callback(Output('databank-graph', 'elements'),
        Input('interval-component', 'n_intervals'),
        Input('databank-graph', 'elements'),
        prevent_initial_call=True,)
        
def update_metrics(n,element):
    global data,trigger_web_hook, device_graph_list,service_graph_list,relation
    if(trigger_web_hook == 1):
        with open('./mock_data.json', 'r') as file:
            datanew = json.load(file)
        data = datanew["data"]
        screen_width = datanew["screenWidth"]
        screen_heigth = 700
        #def devide screen size for device and service
        device_screen_width = int(3*screen_width / 5)
        service_screen_width = int(2*screen_width / 5)
        device_screen_height = service_screen_heigth = screen_heigth

        devices, services = create_elements(data) # get devices and services from data
        home_tree = create_home_tree(devices=devices) # make tree for device
        if home_tree is not None:
            home_tree.print_tree(show_id=True, show_level=True)
        #gen grapg for visual for device
        device_graph_list = []
        if len(devices):
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
        companyTree =[]
        if len(services):
            each_service_height = int(
                (1 / len(services)) * service_screen_heigth
            )
            each_service_width = 1 * service_screen_width

            companyTree = create_company_tree(services=services)
            companyTree.print_tree(show_id=True, show_level=True)

            service_graph_list = companyTree.gen_data_visual_company(
                top_x=service_screen_width,
                top_y=0,
                screen_width=service_screen_width,
                screen_height=service_screen_heigth,
                show_company_node=False,
                home=home_tree,
            ),
            flat_list = []
            for element in service_graph_list:
                flat_list.extend(element)
            service_graph_list = flat_list
            relation = (create_relation_service_device(home=home_tree, company=companyTree))
        trigger_web_hook=0
        data = datanew
        return  (device_graph_list) + (service_graph_list) + relation
    return  element

app.layout = html.Div(
    [
        # html.P(id="tapNode"),
        # html.P(id="tapEdge"),
        # html.P(id="mouseOverNode"),
        # html.P(id="mouseOverEdge"),
        html.Div(id="hover-popup", style={"position": "absolute", "display": "none"}),
        cyto.Cytoscape(
            id="databank-graph",
            layout={"name": "preset", 'spacingFactor': 0.8,},
            style={
                # "width": str(screen_width) + "px",
                # "height": str(screen_heigth) + "px",
                "width": "99%",
                "height": "700px",
                "position": "absolute",
            },
            maxZoom=20,
            minZoom=0.8,
            autolock=False,
            autounselectify=False,
            elements=[],
            stylesheet=stylesheet,
        ),
        dcc.Interval(
            id='interval-component',
            interval=2*1000, # in milliseconds
            n_intervals=0
        ),
    ]
)
# app.clientside_callback(
#     """
#     function(n_intervals) {
#         if (!window.cyInstance) {
#             const cytoscapeDiv = document.querySelector('#databank-graph');
#             let cy = cytoscapeDiv._cyreg.cy;
#             cy.fit();
#         }
#         return '';
#     }
#     """,
#     Output('interval-component', 'children'),
#     Input('databank-graph', 'n_intervals'),
# )
@callback(
    Output("hover-popup", "children"),
    Output("hover-popup", "style"),
    Input("databank-graph", "elements"),
    Input("databank-graph", "tapNode"),
    Input("databank-graph", "tapEdge"),
)
def display_hover_popup(elements,tapNode,tapEdge):
    if tapNode:
        print(tapNode)
        # Content for the popup
        content = f"Node: {tapNode.data.label}"
        # Position the popup based on node position
        style = {
            "display": "block",
            "left": f"{tapNode['renderedPosition']['x'] + 50}px",  # Offset to avoid direct overlap
            "top": f"{tapNode['renderedPosition']['y'] +10}px",
            "backgroundColor": "lightgrey",
            "padding": "5px",
            "position": "absolute",
            "border": "1px solid grey",
            "borderRadius": "5px",
            "zIndex": 1000
        }
        return content, style
    elif tapEdge:
        return "", {"display": "none"}
    return "", {"display": "none"}

@server.route("/webhook", methods=['POST'])
def webhook():
    global trigger_web_hook
    try:
        dataNew = request.get_json()
        with open('mock_data.json', 'w') as file:
            json.dump(dataNew, file, indent=4)
        trigger_web_hook = 1
        return jsonify({"status": "success", "message": f"Processed data success","data": 'success'}), 200
    except Exception as e:
        dataNew = {'data':{'devices':{},'services':{}},'screenWidth':1920}
        return jsonify({"status": "error", "message": str(e)}), 500
# # Create callback when click node
# @callback(Output("tapNode", "children"), Input("databank-graph", "tapNodeData"))
# def displayTapNodeData(data):
#     if data:
#         return f"Tap node data: {data['label']}"
#     else:
#         return "Tap node data: None"


# # Create callback when click edge
# @callback(Output("tapEdge", "children"), Input("databank-graph", "tapEdgeData"))
# def displayTapEdgeData(data):
#     if data:
#         return f"Tap edge data: {data['id']}"
#     else:
#         return "Tap edge data: None"


# # Create callback when mouse over node
# # @callback(
# #     Output("mouseOverNode", "children"), Input("databank-graph", "mouseoverNodeData")
# # )
# # def displayMouseOverNodeData(data):
# #     if data:
# #         return f"Mouse over node data: {data['label']}"
# #     else:
# #         return "Mouse over node data: None"


# # Create callback when mouse over edge
# @callback(
#     Output("mouseOverEdge", "children"), Input("databank-graph", "mouseoverEdgeData")
# )
# def displayMouseOverEdgeData(data):
#     if data:
#         return f"Mouse over edge data: {data['id']}"
#     else:
#         return "Mouse over edge data: None"


if __name__ == "__main__":
    app.run(port=5000,)  # type: ignore
    # app.run(debug=True)
