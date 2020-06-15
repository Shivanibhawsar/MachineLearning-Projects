import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

def Navbar():
     navbar = dbc.NavbarSimple(
          className = "navbar",
           children=[
               dbc.Row(
                [
                    dbc.Col(html.Img(className="coronalogo", src=app.get_asset_url("coronalogo.png"), height="30px")),
                
                ],
                align="center",
                no_gutters=True,
               ),
              dcc.Link('HOME', href='/home', 
         style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold','font-size':'20px','padding':'10px'}),
               dcc.Link('VISUALIZOR', href='/visualize', 
         style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold','font-size':'20px','padding':'10px'},target='_blank'),
               dcc.Link('PREDICTOR', href='/corona-predictor', 
         style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold','font-size':'20px','padding':'10px'},target='_blank'),
               dcc.Link('ABOUT', href='/about', 
         style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold','font-size':'20px','padding':'10px'},target='_blank'),
              
                  ],
          brand="CoronaPredictor",
          brand_href="/home",
          sticky="top",
          color="#292B33",
          dark=True,
          id="navbar"
        )
     return navbar
 
