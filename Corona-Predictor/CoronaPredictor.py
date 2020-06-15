import pandas as pd
import dash
import fbprophet
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objs as go
from homeNavbar import Navbar
import os
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
nav = Navbar()


#output = html.Div(id = 'output',
 #               children = [],
  #              )
output = dcc.Loading(id = "loading-icon", 
                children=[], type="default")

header = html.H3(
    'Select the DISTRICT and Type Of CORONA CASES to see FUTURE PROBABILITY OF CASES!!!'
)

def trainData(district,cases):
    if 'Deaths' in cases:
        case = 'deceased';
    elif 'Active' in cases:
        case = 'active'
    elif 'Recovered' in cases:
        case = 'recovered'
    else:
        case = 'confirmed'
    datafile = os.getcwd() +'/assets/'+'India_district_daily.csv';
    df_district_daily = pd.read_csv(datafile)
    df_district_daily = df_district_daily[df_district_daily['district'].isin([district])]
    gm = df_district_daily.rename(columns={'date': 'ds', case: 'y'})
    gm_prophet = fbprophet.Prophet(changepoint_prior_scale=0.15)
    gm_prophet.fit(gm)
    gm_forecast = gm_prophet.make_future_dataframe(periods=60, freq='D')
    gm_forecast = gm_prophet.predict(gm_forecast)

    yhat = go.Scatter(
      x = gm_forecast['ds'],
      y = gm_forecast['yhat'],
      mode = 'lines',
      marker = {
        'color': '#3bbed7'
      },
      line = {
        'width': 3
      },
      name = 'PREDICTION',
    )
    yhat_lower = go.Scatter(
      x = gm_forecast['ds'],
      y = gm_forecast['yhat_lower'],
      marker = {
        'color': 'rgba(0,0,0,0)'
      },
      showlegend = False,
      hoverinfo = 'none',
    )
    yhat_upper = go.Scatter(
      x = gm_forecast['ds'],
      y = gm_forecast['yhat_upper'],
      fill='tonexty',
      fillcolor = 'rgba(231, 234, 241,.75)',
      name = 'PROBABILITY',
      hoverinfo = 'none',
      mode = 'none'
    )
    actual = go.Scatter(
      x = gm_forecast['ds'],
      y = df_district_daily[case],
      mode = 'markers',
      marker = {
        'color': 'black',
        'size': 4,
        'line': {
          'color': '#000000',
          'width': .75
        }
      },
      name = 'HISTORY CASES'
    )

    layout = go.Layout(
      yaxis = {
        'title': 'CASES',
        'hoverformat': format('y_col')
      },
      hovermode = 'x',
      xaxis = {
        'title': 'DATE'
      },
      margin = {
        't': 20,
        'b': 50,
        'l': 60,
        'r': 10
      },
      legend = {
        'bgcolor': 'rgba(0,0,0,0)'
      }
    )
    data = [yhat_lower, yhat_upper, yhat,actual]
    return data;

def Corona_Predictor(dropdown,dropdown_cases):
    layout = html.Div([
        nav,
        
        header,
        dropdown,
        dropdown_cases,
        output
    ])
    return layout

def build_graph(district,cases):
    if district is not None and cases is not None:
        data = trainData(district,cases)
        graph = dcc.Graph(
                   figure = {
                       'data': data,
                'layout': go.Layout(
                      yaxis = {
                        'title': cases,
                        'tickformat': format('Active'),
                        'hoverformat': format('y_col')
                      },
                      hovermode = 'x',
                      xaxis = {
                        'title': 'DATE'
                      },
                      margin = {
                        't': 20,
                        'b': 50,
                        'l': 60,
                        'r': 10
                      },
                      legend = {
                        'bgcolor': 'rgba(0,0,0,0)'
                      }
                     )
                       }
                     )
        return graph

def removeUnwantedValues(df_district):
    indexNames = df_district[ df_district['district'] == 'Other State' ].index
    df_district.drop(indexNames , inplace=True)
    indexNames = df_district[ df_district['district'] == 'Italians*' ].index
    df_district.drop(indexNames , inplace=True)
    indexNames = df_district[ df_district['district'] == 'Italians' ].index
    df_district.drop(indexNames , inplace=True)
    indexNames = df_district[ df_district['district'] == 'Evacuees' ].index
    df_district.drop(indexNames , inplace=True)
    indexNames = df_district[ df_district['district'] == 'Evacuees*' ].index
    df_district.drop(indexNames , inplace=True)
    indexNames = df_district[ df_district['district'] == 'Others state' ].index
    df_district.drop(indexNames , inplace=True)
    indexNames = df_district[ df_district['district'] == 'Other state' ].index
    df_district.drop(indexNames , inplace=True)
    return df_district;

def districtrender(statename):
    datafile = os.getcwd() +'/assets/'+'India_district_daily.csv'
    #datafile = app.get_asset_url("India_district_daily.csv")
    #datafile = datafile[1:]
    #datafile = datafile.replace('/', '\\')
    df_district = pd.read_csv(datafile)
    df_district = removeUnwantedValues(df_district)
    df_district = df_district[df_district['state'].isin([statename])]
    dis = df_district['district'].unique()
    dis_cases = ['Confirmed Cases' ,'Active Cases', 'Recovered Cases', 'Deaths Cases']
    options = [{'label':x.replace(', Illinois', ''), 'value': x} for x in dis]
    options_cases = [{'label':x.replace(', Illinois', ''), 'value': x} for x in dis_cases]
    dropdown = html.Div(dcc.Dropdown(
        id = 'pop_dropdown',
        options = options,
        placeholder="Select District of "+statename
    ))
    dropdown_cases = html.Div(dcc.Dropdown(
        id = 'pop_dropdown_case',
        options = options_cases,
        placeholder="Select type of Corona Cases"
    ))
    return dropdown, dropdown_cases


