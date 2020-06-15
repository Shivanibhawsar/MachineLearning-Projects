import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

def footerbar():
     navbar = dbc.NavbarSimple(
          className = "footerbar",
           children=[
               
              html.P(className = "footerdata",children = [
                       """GMAIL : shivanibhawsar.11@gmail.com""",html.Br(),

                      ]),
              dcc.Link('LINKEDIN PROFILE', href='https://www.linkedin.com/in/shivanibhawsar',target='_blank', 
              style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold','margin-left':'-220px','margin-top':'20px'})
              ,    
          dcc.Link('FORM FOR FEEDBACK OR QUESTIONS', href='https://forms.gle/PaVPaMzwvMrLBjsi7',target='_blank', 
         style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold','margin-left':'-210px','margin-top':'38px'}),
          ],
          color="#292B33",
          dark=True,
          sticky="bottom",
          id="footerbar"
        )
     return navbar
 
