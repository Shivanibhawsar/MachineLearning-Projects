import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from homeNavbar import Navbar
from footer import footerbar

#Initialize Header and Footer
nav = Navbar()
foot = footerbar()

#Initialize Dash app
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.config.suppress_callback_exceptions = True

#Set main Content
body = dbc.Container(
    [
       dbc.Row(
           [
               dbc.Col(
                  [
                     html.H2("PLAN FOR FUTURE,FIGHT FOR FUTURE"),
                     html.P(
                         """\
Visualize and Predict Future Corona Cases in advance, and finally plan for future to fight for future. You can Visualize current situation and predict for FUTURE corona cases in different Districts and States of India. So Let's Visualize with Visualizor and Predict with Predictor"""
                           ),
                           html.A(html.Button('VISUALIZOR',className='Visualizor'),
    href='/visualize',target='_blank'),
                        html.A(html.Button('PREDICTOR', className='Predictor'),
    href='/corona-predictor',target='_blank')
                   ],
                  md=4,
               ),
              dbc.Col(
                 [
                     html.H2("Visualize and Predict Corona Cases"),
                     html.Img(
                            className="logo1", src=app.get_asset_url("homeImage1.png")
                        ),
                        ]
                     ),
                ]
            )
       ],
className="mt-4",
)



#define MainFunction to call
def Homepage():
    layout = html.Div([
    nav,
    body,
    foot
    ])
    return layout




    
