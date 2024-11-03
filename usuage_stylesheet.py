import dash
from dash import dcc, html, no_update
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)

# Sample network data
network_data = {
    "nodes": [{"id": 1, "label": "Node 1"}, {"id": 2, "label": "Node 2"}],
    "edges": [{"source": 1, "target": 2}]
}

app.layout = html.Div([
    dcc.Graph(id="network-graph"),
    dcc.Store(id='node-data')
])

@app.callback(
    [Output('node-data', 'data'), Output('network-graph', 'figure')],
    Input('network-graph', 'clickData')
)
def update_graph(node_data):
    if node_data is None:
        return {}, {}

    selected_node_id = node_data['points'][0]['pointNumber']

    # Show modal window with node details
    modal_content = html.Div([
        html.H1(selected_node_id),
        html.P("Some other information about this node"),
        html.Button('Close', id='close-button')
    ])

    return {'node-id': selected_node_id}, {
        "data": network_data["nodes"],
        'layout': {
            'xaxis': {'visible': False},
            'yaxis': {'visible': False}
        }
    }

@app.callback(
    Output("network-graph", "figure"),
    [Input('close-button', 'n_clicks')]
)
def close_modal(n_clicks):
    if n_clicks:
        return {
            "data": network_data["nodes"],
            'layout': {
                'xaxis': {'visible': False},
                'yaxis': {'visible': False}
            }
        }

if __name__ == "__main__":
    app.run_server(debug=True)