from icecream import ic
from graph_constants import *
# from mock_data import data
from graph_utils import create_elements, create_home_tree, create_company_tree, create_relation_service_device
from graph_style import stylesheet   


# TODO: making graph
from dash import dcc, Dash, html, Input, Output, State, callback, no_update
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

data= {'data':{'devices':{},'services':{}},'screenWidth':1920}
trigger_web_hook = 0
trigger_filter_change = 0
reset_filter_change = 0
filter_type = [None,None,None,None]
device_graph_list = []
service_graph_list = []
relation = []
device_name = []
device_data = []
service_name = []
service_type = []
new_value = [None,None,None,None]
old_element = []
server = Flask(__name__)
app = Dash(__name__, server=server)
CORS(server)

default_stylesheet = [{'selector': 'edge', 'style': {'curve-style': 'bezier'}}, {'selector': '.home', 'style': {'background-color': '#3498db', 'content': 'data(label)'}}, {'selector': '.device_normal', 'style': {'background-color': '#148f77', 'content': 'data(label)'}}, {'selector': '.device_special', 'style': {'background-color': '#f39c12', 'content': 'data(label)'}}, {'selector': '.company', 'style': {'background-color': '#592720', 'content': 'data(label)'}}, {'selector': '.service_normal', 'style': {'background-color': '#e53145', 'content': 'data(label)'}}, {'selector': '[id *= "relation_"]', 'style': {'line-color': 'black', 'target-arrow-color': 'black', 'target-arrow-shape': 'triangle'}}]
# update function when new data
@callback(
        Output('databank-graph', 'elements'),
        Output('device', 'options'),
        Output('device_data', 'options'),
        Output('service_name', 'options'),
        Output('service_type', 'options'),
        Input('interval-component', 'n_intervals'),
        Input('databank-graph', 'elements'),
        prevent_initial_call=True,)
        
def update_metrics(n,element):
    global data,trigger_web_hook,device_graph_list,service_graph_list,relation,device_name,device_data,service_name,service_type,trigger_filter_change,new_value,filter_type,reset_filter_change
    #filter graph
    if trigger_filter_change==1:
        # make element to default
        no_filter_data= []
        for data in element:
            data['classes'] = data['classes'].replace(' not_select', '')
            no_filter_data.append(data.copy())
        data_element = []
        use_element = []
        use_element = element.copy()
        if filter_type[0] != None:
            data=[]
            company_pair = []
            new_element = use_element.copy()[::-1]
            for result in new_element:
                if ' not_select' in result['classes']:
                    result['classes'] = result['classes'].replace(' not_select', '')
                if result['classes'] == 'device_relation':
                    if not ('d_'+new_value[0] in str(result['data']['target']) and 'd_'+new_value[0] in str(result['data']['source'])) :
                        result['classes'] = result['classes']+" not_select"
                if result['classes'] == 'between_relation':
                    if 'd_'+new_value[0] in str(result['data']['target']):
                        company_pair.append(result['data']['source'])
                    else:
                        result['classes'] = result['classes']+" not_select"
                elif result['classes'] == 'device_normal' or result['classes'] == 'between_relation' or result['classes'] == 'device_special':
                    if 'd_'+new_value[0] not in str(result['data']['id']) and len([item for item in company_pair if item in str(result['data']['id'])])==0:
                        result['classes'] = result['classes']+" not_select"
                data.append(result.copy())
            new_data = []
            for result in data:
                if result['classes'] == 'service_relation':
                    if len([item for item in company_pair if item in result['data']['target']])>0:
                        company_pair.append(result['data']['source'])
                    else:
                        result['classes'] = result['classes']+" not_select"
                if result['classes'] == 'service_normal':
                    if len([item for item in company_pair if item in result['data']['id']])>0:
                        company_pair.append(result['data']['id'])
                    else:
                        result['classes'] = result['classes']+" not_select"
                new_data.append(result.copy())
            new_data = new_data[::-1]
            data_element.append(new_data.copy())
        else:
            data_element.append(use_element.copy())
        if filter_type[1] != None:
            data=[]
            company_pair = []
            new_element = use_element.copy()[::-1]
            for result in new_element:
                if ' not_select' in result['classes']:
                    result['classes'] = result['classes'].replace(' not_select', '')
                if result['classes'] == 'device_relation':
                    if new_value[1] in str(result['data']['target']) and new_value[1] not in str(result['data']['source']):
                        company_pair.append(result['data']['source'])
                    elif not (new_value[1] in str(result['data']['target']) and new_value[1] in str(result['data']['source'])) :
                        result['classes'] = result['classes']+" not_select"
                if result['classes'] == 'between_relation':
                    if new_value[1] in str(result['data']['target']):
                        company_pair.append(result['data']['source'])
                    else:
                        result['classes'] = result['classes']+" not_select"
                elif result['classes'] == 'device_normal' or result['classes'] == 'between_relation' or result['classes'] == 'device_special':
                    if new_value[1] not in str(result['data']['id']) and len([item for item in company_pair if item in str(result['data']['id'])])==0:
                        result['classes'] = result['classes']+" not_select"
                data.append(result.copy())
            new_data = []
            for result in data:
                if result['classes'] == 'device_normal':
                    if new_value[1] not in str(result['data']['id']) and len([item for item in company_pair if item == str(result['data']['id'])])==0:
                        result['classes'] = result['classes']+" not_select"
                if result['classes'] == 'service_relation':
                    if len([item for item in company_pair if item in result['data']['target']])>0:
                        company_pair.append(result['data']['source'])
                    else:
                        result['classes'] = result['classes']+" not_select"
                if result['classes'] == 'service_normal':
                    if len([item for item in company_pair if item in result['data']['id']])>0:
                        company_pair.append(result['data']['id'])
                    else:
                        result['classes'] = result['classes']+" not_select"
                new_data.append(result.copy())
            new_data = new_data[::-1]
            data_element.append(new_data.copy())
        else:
            data_element.append(use_element.copy())
        if filter_type[2] != None:
            data=[]
            device_pair = []
            new_element = use_element.copy()[::-1]
            for result in new_element:
                if ' not_select' in result['classes']:
                    result['classes'] = result['classes'].replace(' not_select', '')
                if result['classes'] == 'service_relation':
                    if not ('s_'+new_value[2] in str(result['data']['source']) and 's_'+new_value[2] in str(result['data']['target'])) :
                        result['classes'] = result['classes']+" not_select"
                if result['classes'] == 'between_relation':
                    if 's_'+new_value[2] in str(result['data']['source']):
                        device_pair.append(result['data']['target'])
                    else:
                        result['classes'] = result['classes']+" not_select"
                elif result['classes'] == 'service_normal' or result['classes'] == 'between_relation':
                    if 's_'+new_value[2] not in str(result['data']['id']) and len([item for item in device_pair if item in str(result['data']['id'])])==0:
                        result['classes'] = result['classes']+" not_select"
                data.append(result.copy())
            new_data = []
            for result in data:
                if result['classes'] == 'device_normal':
                    if len([item for item in device_pair if item in result['data']['id']])>0:
                        device_pair.append(result['data']['id'])
                    else:
                        result['classes'] = result['classes']+" not_select"
                if result['classes'] == 'device_relation':
                    if len([item for item in device_pair if item in result['data']['target']])>0:
                        device_pair.append(result['data']['source'])
                    else:
                        result['classes'] = result['classes']+" not_select"
                if result['classes'] == 'device_special':
                    if 's_'+new_value[2] not in str(result['data']['id']) and len([item for item in device_pair if item in str(result['data']['id'])])==0:
                        result['classes'] = result['classes']+" not_select"
                new_data.append(result.copy())
            new_data = new_data[::-1]
            data_element.append(new_data.copy())
        else:
            data_element.append(use_element.copy())
        if filter_type[3] != None:
            data=[]
            device_pair = []
            new_element = use_element.copy()[::-1]
            for result in new_element:
                if ' not_select' in result['classes']:
                    result['classes'] = result['classes'].replace(' not_select', '')
                if result['classes'] == 'service_relation':
                    if not (new_value[3] in str(result['data']['source']) and new_value[3] in str(result['data']['target'])) :
                        if new_value[3] in str(result['data']['target']) or len([item for item in device_pair if item in result['data']['target']])>0:
                            device_pair.append(result['data']['source'])
                        else:
                            result['classes'] = result['classes']+" not_select"
                if result['classes'] == 'between_relation':
                    if new_value[3] in str(result['data']['source']):
                        device_pair.append(result['data']['target'])
                    else:
                        result['classes'] = result['classes']+" not_select"
                elif result['classes'] == 'service_normal' or result['classes'] == 'between_relation':
                    if new_value[3] not in str(result['data']['id']) and len([item for item in device_pair if item in str(result['data']['id'])])==0:
                        result['classes'] = result['classes']+" not_select"
                data.append(result.copy())
            new_data = []
            for result in data:
                # if result['classes'] == 'service_relation not_select':
                #     if len([item for item in device_pair if item in result['data']['target']])>0:
                #         result['classes'] = result['classes'].replace(' not_select','')
                #         device_pair.append(result['data']['source'])
                # if result['classes'] == 'service_normal not_select':
                #     if len([item for item in device_pair if item in str(result['data']['id'])])>0:
                #         result['classes'] = result['classes'].replace(' not_select','')
                #         device_pair.append(result['data']['id'])
                if result['classes'] == 'device_normal':
                    if len([item for item in device_pair if item in result['data']['id']])>0:
                        device_pair.append(result['data']['id'])
                    else:
                        result['classes'] = result['classes']+" not_select"
                if result['classes'] == 'device_relation':
                    if len([item for item in device_pair if item in result['data']['target']])>0:
                        device_pair.append(result['data']['source'])
                    else:
                        result['classes'] = result['classes']+" not_select"
                if result['classes'] == 'device_special':
                    if 's_'+new_value[3] not in str(result['data']['id']) and len([item for item in device_pair if item in str(result['data']['id'])])==0:
                        result['classes'] = result['classes']+" not_select"
                new_data.append(result.copy())
            new_data = new_data[::-1]
            data_element.append(new_data.copy())
        else:
            data_element.append(use_element.copy())
        index = 0
        show_element = []
        for data in use_element:
            if not(data_element[0][index] == data_element[1][index]  == data_element[2][index] == data_element[3][index]):
                data['classes'] = data['classes']+" not_select"
            show_element.append(data)
            index += 1
        element = show_element
        trigger_filter_change=0
    if reset_filter_change == 1:
        data = []
        for result in element:
            if ' not_select' in result['classes']:
                result['classes'] = result['classes'].replace(' not_select', '')
            data.append(result.copy())
        element = data
        reset_filter_change = 0
    if(trigger_web_hook == 1):
        with open('./mock_data.json', 'r') as file:
            datanew = json.load(file)
        data = datanew["data"]
        screen_width = datanew["screenWidth"]
        screen_heigth = datanew["screenHeight"]
        #def devide screen size for device and service
        device_screen_width = int(3*screen_width / 5)
        service_screen_width = int(2*screen_width / 5)
        device_screen_height = service_screen_heigth = screen_heigth

        devices, services = create_elements(data) # get devices and services from data
        # get device name and device_data
        device_name = []
        device_data = []
        for key in datanew['data']['devices'].keys():
            name = datanew['data']['devices'][key]['device_name']
            device_name.append({'label': name, 'value': key})
            if datanew['data']['devices'][key]['device_unprocessed'] != None:
                for data in datanew['data']['devices'][key]['device_unprocessed']:
                    device_data.append({'label': data, 'value': data})
        service_name = []
        service_type = []
        for key in datanew['data']['services'].keys():
            name = datanew['data']['services'][key]['service_name']
            com_type = datanew['data']['services'][key]['service_type']
            service_name.append({'label': name, 'value': key})
            service_type.append({'label': com_type, 'value': com_type})
        # make array unique
        unique_list = []
        [unique_list.append(item) for item in device_name if item not in unique_list]
        device_name = unique_list
        unique_list = []
        [unique_list.append(item) for item in device_data if item not in unique_list]
        device_data = unique_list
        unique_list = []
        [unique_list.append(item) for item in service_name if item not in unique_list]
        service_name = unique_list
        unique_list = []
        [unique_list.append(item) for item in service_type if item not in unique_list]
        service_type = unique_list
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

        # prepare node for service
        service_graph_list = []
        companyTree =[]
        if len(services):
            companyTree = create_company_tree(services=services)
            companyTree.print_tree(show_id=True, show_level=True)
            # get service node and edge element to generate graph
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
            # create relation edge
            relation = (create_relation_service_device(home=home_tree, company=companyTree))
        trigger_web_hook=0
        data = datanew
        return (device_graph_list) + (service_graph_list) + relation,device_name,device_data,service_name,service_type
    return  element,device_name,device_data,service_name,service_type

app.layout = html.Div(
    [
        html.Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"),
        html.Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/select2/4.1.0/select2.min.css"),
        html.Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/select2-bootstrap-5-theme/1.4.0/select2-bootstrap.min.css"),
        html.Script(src="https://code.jquery.com/jquery-3.6.4.min.js"),
        html.Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"),
        html.Script(src="https://cdnjs.cloudflare.com/ajax/libs/select2/4.1.0/select2.min.js"),
        # popup element
        html.Div(id="node-popup", style={"position": "absolute", "display": "none"}),
        html.Div(id="edge-popup", style={"position": "absolute", "display": "none"}),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id='device',
                            options=[],
                            value=None,  # Default selected value
                            placeholder="Select a device",  # Placeholder text
                        ),
                    ],
                    style={
                    'width':'23%',
                    'padding':'10px',
                }),
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id='device_data',
                            options=[],
                            value=None,  # Default selected value
                            placeholder="Select a device data",  # Placeholder text
                        ),
                    ],
                    style={
                    'width':'23%',
                    'padding':'10px',
                }),
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id='service_name',
                            options=[],
                            value=None,  # Default selected value
                            placeholder="Select an service name",  # Placeholder text
                        ),
                    ],
                    style={
                    'width':'23%',
                    'padding':'10px',
                }),
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id='service_type',
                            options=[],
                            value=None,  # Default selected value
                            placeholder="Select an service detail",  # Placeholder text
                        ),
                    ],
                    style={
                    'width':'23%',
                    'padding':'10px',
                }),
                html.Div(
                    children=[
                        html.Button('Reset', id='clear_filter',className='btn btn-primary')
                    ],
                    style={
                    'width':'8%',
                    'padding':'10px',
                }),
            ],
            style={
                "display":"flex",
            },
        ),
        # show graph
        cyto.Cytoscape(
            id="databank-graph",
            layout={"name": "preset", 'spacingFactor': 0.8,},
            style={
                "width": "99%",
                "height": "882px",
                "position": "absolute",
            },
            maxZoom=20,
            minZoom=0.1,
            autolock=False,
            autounselectify=False,
            elements=[],
            stylesheet=stylesheet,
            boxSelectionEnabled=True
        ),
        # element update graph
        dcc.Interval(
            id='interval-component',
            interval=2*1000, 
            n_intervals=0
        ),
    ]
)
# select filter
@app.callback(
    Input("device",'value'),
    Input("device_data",'value'),
    Input("service_name",'value'),
    Input("service_type",'value'),
    prevent_initial_call=True
)
def device_name_click(value,value_data,value_company,value_type):
    global new_value,trigger_filter_change,filter_type,reset_filter_change
    # select device name
    if value != None:
        new_value[0] = value
        filter_type[0] = 'device'
    else:
        new_value[0] = None
        filter_type[0] = None
    # select device data
    if value_data != None:
        new_value[1] = value_data.replace(' ','_')
        filter_type[1] = 'device_data'
    else:
        new_value[1] = None
        filter_type[1] = None
    # select company name
    if value_company != None:
        new_value[2] = value_company
        filter_type[2] = 'service_name'
    else:
        new_value[2] = None
        filter_type[2] = None
    # select company type
    if value_type != None:
        new_value[3] = value_type.replace(' ','_')
        filter_type[3] = 'service_type'
    else:
        new_value[3] = None
        filter_type[3] = None
    trigger_filter_change = 1

# select company type
@app.callback(
    Output("device",'value'),
    Output("device_data",'value'),
    Output("service_name",'value'),
    Output("service_type",'value'),
    Input("clear_filter",'n_clicks'),
    prevent_initial_call=True
)
def button_click(value):
    global reset_filter_change
    reset_filter_change = 1
    return None,None,None,None
# function show popup when select
@app.callback(
    [
        Output("node-popup", "children"),
        Output("node-popup", "style"),
        Output("edge-popup", "children"),
        Output("edge-popup", "style"),
        Output('databank-graph', 'selectedNodeData'),
        Output('databank-graph', 'selectedEdgeData')
    ],
    [
        Input("databank-graph", "tapNode"),
        Input("databank-graph", "tapEdge"),
        State("databank-graph", "elements"),
        Input('databank-graph', 'selectedNodeData'),
        Input('databank-graph', 'selectedEdgeData'),
        State("edge-popup", "style")
    ],
)
def display_hover_popup(tapNode,tapEdge,elements,selectedNodeData,selectedEdgeData,style_edge):
    if selectedNodeData:
        # Content for the popup
        content = f"Node: {tapNode['data']['label']}"
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
            "zIndex": 1000,
            "width": "150px",  
            "whiteSpace": "normal",
            "overflowWrap": "break-word",
        }
        return  content, style,"", {"position":"absolute","display": "none"},None,None
    elif selectedEdgeData:
        # Calculate the midpoint of the edge
        source_node = next(el for el in elements if el['data']['id'] == tapEdge['data']['source'])
        target_node = next(el for el in elements if el['data']['id'] == tapEdge['data']['target'])

        source_pos = source_node['position']
        target_pos = target_node['position']

        midpoint_x = (source_pos['x'] + target_pos['x']) / 2
        midpoint_y = (source_pos['y'] + target_pos['y']) / 2

        # Popup content and position for an edge
        content = f"Edge: {tapEdge['data']['id']}"
        style = style_edge.copy()
        style.update({
            "display": "block",
            "left": f"{midpoint_x + 50}px",  
            "top": f"{midpoint_y + 10}px",
            "backgroundColor": "lightgrey",
            "padding": "5px",
            "position": "absolute",
            "border": "1px solid grey",
            "borderRadius": "5px",
            "zIndex": 1000,
            "width": "250px",  # Set a fixed width
            "whiteSpace": "normal",  # Allow text to wrap
            "overflowWrap": "break-word",
        })
        return "", {"position":"absolute","display": "none"},content, style,None,None
    return "", {"position":"absolute","display": "none"},"", {"position":"absolute","display": "none"},None,None



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


if __name__ == "__main__":
    # app.run(port=5000,)  # type: ignore
    app.run(debug=True)
