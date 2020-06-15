import json
import base64
import datetime
import requests
import pathlib
import math
import pandas as pd
import numpy as np
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from homeNavbar import Navbar
from dash.dependencies import Input, Output, State
from plotly import tools
from DistrictDailyDataAPI import fetchLatestData
from Predictor import state_predictor,fetchAPI
import sys


nav = Navbar()


output_pieconfirmedgraph = html.Div(className = "output_pieconfirmedgraph",id = 'output_pieconfirmedgraph',
                children = [],
                )
output_pierecoveredgraph = html.Div(className = "output_pierecoveredgraph",id = 'output_pierecoveredgraph',
                children = [],
                )
output_pieactivegraph = html.Div(className = "output_pieactivegraph",id = 'output_pieactivegraph',
                children = [],
                )
output_piedeceasedgraph = html.Div(className = "output_piedeceasedgraph",id = 'output_piedeceasedgraph',
                children = [],
                )
output_bargraph = html.Div(className = "output_bargraph",id = 'output_bargraph',
                children = [],
                )
output_linegraph = html.Div(className = "output_linegraph",id = 'output_linegraph',
                children = [],
                )

header = html.H3(
    'Select the STATE of India to see corona cases!!!!'
)

def Corona_Visualizor(state_dropdown):
    layout = html.Div([
        nav,
        header,
        state_dropdown,
        output_bargraph,
        output_linegraph,
        output_pieconfirmedgraph,
        output_pieactivegraph,
        output_pierecoveredgraph,
        output_piedeceasedgraph
    ])
    return layout

def fetchstateAPI(state):
    response = requests.get('https://api.covid19india.org/v2/state_district_wise.json')
    content = response.content
    parsed = json.loads(content)
    dfs = []
    for i in parsed:
        state_name = i['state']
        state_code = i['statecode']
        df = pd.DataFrame(i['districtData'])
        df['state name'] = state_name
        df['state code'] = state_code
        dfs.append(df)
    district_level = pd.concat(dfs)
    district_level = district_level[['state name', 'state code', 'district', 
                                 'confirmed', 'active', 'deceased', 'recovered'
                            ]]
    district_level = district_level[district_level['state name'].isin([state])]
    return district_level;
       
def visualize_bargraph(state):
    if state is not None:
        df_state = fetchstateAPI(state)
        fig = go.Figure(data=[
        go.Bar(name='CONFIRMED',x= df_state['district'],y=df_state['confirmed']),
        go.Bar(name='ACTIVE',x=df_state['district'],y=df_state['active'])
        ])
        fig.update_layout(barmode='stack')
        fig.layout.plot_bgcolor = "#1A1C23";
        fig.layout.paper_bgcolor = "#1A1C23";
        fig.update_layout(
        title="Corona Cases For "+state,
        xaxis_title="DISTRICTS",
        yaxis_title="CASES",
        font=dict(
            size=16,
            color="#DCF7F7"
        )
        )
        fig2 = dcc.Graph(
            figure=fig
        )
        return fig2

def visualize_linegraph(state):
    if state is not None:
        df_state = fetchstateAPI(state)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_state['district'],
            y=df_state['confirmed'],
            
            line_color='#0557EB',
            name='Confirmed',
        ))
        fig.add_trace(go.Scatter(
            x=df_state['district'],
            y=df_state['active'],
            line_color='#E63C12',
            name='Active',
        ))
        fig.add_trace(go.Scatter(
            x=df_state['district'],
            y=df_state['recovered'],
            line_color='#A3F23D',
            name='Recovered',
        ))
        fig.add_trace(go.Scatter(
            x=df_state['district'],
            y=df_state['deceased'],
            line_color='#ED3BEF',
            name='Deceased',
        ))

        fig.update_traces(mode='lines')
        fig.layout.plot_bgcolor = "#1A1C23";
        fig.layout.paper_bgcolor = "#1A1C23";
        fig.update_layout(
        xaxis_title="DISTRICTS",
        yaxis_title="CASES",
        font=dict(
            
            size=16,
            color="#DCF7F7"
        )
        )
        fig2 = dcc.Graph(
            figure=fig
        )
        
        return fig2
    
def visualize_pieconfirmedgraph(state):
    if state is not None:
        df_state = fetchstateAPI(state)
        data = [
        {
            'values': df_state['confirmed'],
            'type': 'pie',
            'labels': df_state['district']
        },
        ]
        fig = dcc.Graph(
            id='graph',
            figure={
                'data': data,
                'layout': {
                "paper_bgcolor": "#1A1C23",
                "plot_bgcolor": "#1A1C23",
                 "title":"Confirmed Cases For "+state,
            "font":dict(
            
                size=14,
                color="#DCF7F7"
            )
                }
            }
        )
        return fig

def visualize_pierecoveredgraph(state):
    if state is not None:
        df_state = fetchstateAPI(state)
        data = [
        {
            'values': df_state['recovered'],
            'type': 'pie',
            'labels': df_state['district']
        },
        ]
        fig = dcc.Graph(
            id='graph',
            figure={
                'data': data,
                'layout': {
                "paper_bgcolor": "#1A1C23",
                "plot_bgcolor": "#1A1C23",
                 "title":"Recovered Cases For "+state,
            "font":dict(
            
                size=14,
                color="#DCF7F7"
            )
                }
            }
        )
        return fig

def visualize_pieactivegraph(state):
    if state is not None:
        df_state = fetchstateAPI(state)
        data = [
        {
            'values': df_state['active'],
            'type': 'pie',
            'labels': df_state['district']
        },
        ]
        fig = dcc.Graph(
            id='graph',
            figure={
                'data': data,
                'layout': {
                "paper_bgcolor": "#1A1C23",
                "plot_bgcolor": "#1A1C23",
                 "title":"Active Cases For "+state,
            "font":dict(
            
                size=14,
                color="#DCF7F7"
            )
                }
            }
        )
        return fig

def visualize_piedeceasedgraph(state):
    if state is not None:
        df_state = fetchstateAPI(state)
        data = [
        {
            'values': df_state['deceased'],
            'type': 'pie',
            'labels': df_state['district']
        },
        ]
        fig = dcc.Graph(
            id='graph',
            figure={
                'data': data,
                'layout': {
                "paper_bgcolor": "#1A1C23",
                "plot_bgcolor": "#1A1C23",
                 "title":"Deceased Cases For "+state,
            "font":dict(
            
                size=14,
                color="#DCF7F7"
            )
                }
            }
        )
        return fig


def staterender():
    df_state = fetchAPI()
    dis = df_state['state'].unique()
    index = np.argwhere(dis=='Total')
    dis = np.delete(dis, index)
    index = np.argwhere(dis=='State Unassigned')
    dis = np.delete(dis, index)
    options = [{'label':x.replace('State Unassigned', ''), 'value': x} for x in dis]
    state_dropdown = html.Div(dcc.Dropdown(
        id = 'state_dropdown',
        options = options,
        placeholder="Select STATE"
    ))
    return state_dropdown
    





    
