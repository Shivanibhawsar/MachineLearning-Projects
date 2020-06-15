import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from homeNavbar import Navbar

#Initialize Header
nav = Navbar()
#Initialize Dash app
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])

#set body
body = dbc.Container(
    [
       dbc.Row(
           [
                     html.H2("PLAN FOR FUTURE,FIGHT FOR FUTURE"),
                     html.P(
                        [ """\
    CORONAPREDICTOR.com is an online dashboard to visualize and predict the corona cases on a daily basis in different districts of India.""", html.Br(),
    html.Br(),
    """It acts as a online portal for the public to keep track of the latest number of corona cases in different regions of India.""",html.Br(),
    html.Br(),
    """The main functionality of this portal is to predict future corona cases in advance and plan to fight with corona. We can predict the probability of corona cases in different regions of India and plan our work life based on the condition. It is collecting data on daily basis and works as dynamic application which update itself based on the conditions""",html.Br(),
    html.Br(),
    """So, let’s predict the cases and plan for future to fight with future""",
    html.Br(),
    html.Br(),
    """If you want to give any feedback or have any kind of questions, Please fill this form or you can reach out to me on my Gmail ID""",html.Br(),
                          """shivanibhawsar.11@gmail.com"""
                          ]),
                        dcc.Link('FORM FOR FEEDBACK OR QUESTIONS', href='https://forms.gle/PaVPaMzwvMrLBjsi7',target='_blank', 
         style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold'})
                               
                       
                  
                  
           ],
    className="mt-4",
    )
           ]
        )

#Define Main Function
def Aboutpage():
    layout = html.Div([
    nav,
    body
    ])
    return layout

    
