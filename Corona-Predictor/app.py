import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask, send_from_directory
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from HomePage import Homepage
from CoronaPredictor import Corona_Predictor, build_graph, districtrender
from Predictor import *
from Visualizor import *
from About import Aboutpage
import os.path
from Tasks import *
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))



server = Flask(__name__, static_folder='static')
app = dash.Dash(__name__, server=server,external_stylesheets=[dbc.themes.UNITED])
app.config.suppress_callback_exceptions = True
app.title = "Corona Predictor"



app.scripts.append_script({"external_url": [
        "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"
]})

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])




@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home' or pathname == '/':
        return Homepage()
    elif pathname == '/about':
        return Aboutpage()
    elif pathname =='/corona-predictor':
        return state_predictor()
    elif pathname is None or pathname == '/':
        return 'Loading...'
    elif pathname == '/visualize':
        state_dropdown = staterender()
        return Corona_Visualizor(state_dropdown)
    else:
        pathname = pathname.replace('%20', ' ')
        statename = pathname.replace('/', '')
        dropdown, dropdown_cases = districtrender(statename)
        return Corona_Predictor(dropdown,dropdown_cases)

@app.callback(
    Output('loading-icon', 'children'),
    [Input('pop_dropdown', 'value'),
     Input('pop_dropdown_case', 'value')]
)
def update_graph(district,cases):
    graph = build_graph(district,cases)
    return graph


@app.callback(
    Output('output_bargraph', 'children'),
    [Input('state_dropdown', 'value')
     ]
)
def update_graph(state):
    graph = visualize_bargraph(state)
    return graph

@app.callback(
    Output('output_pieconfirmedgraph', 'children'),
    [Input('state_dropdown', 'value')
     ]
)
def update_graph(state):
    graph = visualize_pieconfirmedgraph(state)
    return graph


@app.callback(
    Output('output_linegraph', 'children'),
    [Input('state_dropdown', 'value')
     ]
)
def update_graph(state):
    graph = visualize_linegraph(state)
    return graph

@app.callback(
    Output('output_pierecoveredgraph', 'children'),
    [Input('state_dropdown', 'value')
     ]
)
def update_graph(state):
    graph = visualize_pierecoveredgraph(state)
    return graph

@app.callback(
    Output('output_pieactivegraph', 'children'),
    [Input('state_dropdown', 'value')
     ]
)
def update_graph(state):
    graph = visualize_pieactivegraph(state)
    return graph

@app.callback(
    Output('output_piedeceasedgraph', 'children'),
    [Input('state_dropdown', 'value')
     ]
)
def update_graph(state):
    graph = visualize_piedeceasedgraph(state)
    return graph


@app.callback(Output("cases", "children"), [Input("i_news", "n_intervals")])
def update_cases_div(n):
    return update_cases()

@server.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(server.root_path, 'static'),
                                     'favicon.ico')

if __name__ == "__main__":
    backgroundUpdateData()
    app.run_server(debug=True)








