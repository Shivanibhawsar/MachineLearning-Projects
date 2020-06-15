# -*- coding: utf-8 -*-
import json
import requests
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from homeNavbar import Navbar

nav = Navbar()
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])


def get_top_bar_cell(cellTitle, cellValue,row):
    return html.Div(
        className="two-col"+row,
        children=[
            html.P(className="p-top-bar", children=cellTitle),
            html.P(className="p-top-bar2", children=cellValue),
            
        ],
    )

def get_top_bar(
    confirmed, active, deaths, recovered
):
    return [
        get_top_bar_cell("CONFIRMED", confirmed,"1"),
        get_top_bar_cell("ACTIVE", active,"2"),
        get_top_bar_cell("DEATHS", deaths,"3"),
        get_top_bar_cell("RECOVERED", recovered,"4"),
        
    ]

def fetchAPI():
    response = requests.get('https://api.covid19india.org/data.json')
    content = response.content
    parsed = json.loads(content)
    national = pd.DataFrame(parsed['cases_time_series'])
    state_level = pd.DataFrame(parsed['statewise'])
    state_level = state_level[['state', 'statecode', 'lastupdatedtime',  
                           'confirmed', 'active', 'deaths', 'recovered']]
    df = pd.DataFrame(state_level)
    indexNames = df[ df['state'] == 'State Unassigned' ].index
    df.drop(indexNames , inplace=True)
    return df;


def update_cases():
    df = fetchAPI();
    Confirmed = df['confirmed'][0]
    Active = df['active'][0]
    Deaths = df['deaths'][0]
    Recovered = df['recovered'][0]
    df = df.iloc[1:]
    
    new_row = pd.DataFrame({'state':'STATE', 'statecode':'STATECODE', 'lastupdatedtime':'LAST UPDATED', 
                            'confirmed':'CONFIRMED', 'active':'ACTIVE', 'deaths':'DEATHS', 
                            'recovered':'RECOVERED'}, index =[0]) 
    df = pd.concat([new_row, df]).reset_index(drop = True) 
    max_rows = 40
    return html.Div(
        children=[
            
            
            html.Div(
                    id="top_bar", className="row div-top-bar", children=get_top_bar(Confirmed,Active,Deaths,Recovered)
                ),
           
            html.Table(
                className="table-cases",
                children=[
                    html.Tr(
                        children=[
                            html.Td(
                                children=[
                                    html.A(
                                        className="td-cases"+df.iloc[i]["state"],
                                        children=df.iloc[i]["state"],
                                        href=df.iloc[i]["state"],
                                        
                                    )
                                ]
                            ),
                             html.Td(
                                children=[
                                    html.P(
                                        className="td-cases",
                                        children=df.iloc[i]["statecode"],
                                       
                                    )
                                ]
                            ),
                             html.Td(
                                children=[
                                    html.P(
                                        className="td-cases",
                                        children=df.iloc[i]["lastupdatedtime"],
                                        
                                    )
                                ]
                            ),
                            html.Td(
                                children=[
                                    html.P(
                                        className="td-cases",
                                        children=df.iloc[i]["confirmed"],
                                    )
                                ]
                            ),
                            html.Td(
                                children=[
                                    html.P(
                                        className="td-cases",
                                        children=df.iloc[i]["active"],
                                    )
                                ]
                            ),
                            html.Td(
                                children=[
                                    html.P(
                                        className="td-cases",
                                        children=df.iloc[i]["deaths"],
                                    )
                                ]
                            ),
                            html.Td(
                                children=[
                                    html.P(
                                        className="td-cases",
                                        children=df.iloc[i]["recovered"],
                                    )
                                ]
                            )
                        ]
                    )
                    for i in range(min(len(df), max_rows))
                ]
            )
        ]
    )


# Dash App Layout
layout = html.Div(
    
    children=[
        nav,
        dcc.Interval(id="interval", interval=1 * 1000, n_intervals=0),
        dcc.Interval(id="fetchAPI", interval=86400, n_intervals=0),
        dcc.Interval(id="i_news", interval=1 * 60000, n_intervals=0),
        dcc.Location(id = 'url', refresh = False),
        html.Div(
            className="three columns div-left-panel",
            children=[
                html.Div(
                    className="div-info",
                    children=[
                        html.Img(
                            className="logo", src=app.get_asset_url("coronalogo.png")
                        ),
                        html.H6(className="title-header", children="FOREX TRADER"),
                        html.P(
                            """
                            """
                        ),
                    ],
                ),
                html.Div(
                    className="div-cases",
                    children=[html.Div(id="cases", children=update_cases())],
                ),
            ],
        )
        ]    
)

def state_predictor():
    return layout;


