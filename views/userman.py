# Dash configuration
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from server import app

# Create app layout
layout = html.Div(children=[
    dcc.Location(id='url_userman', refresh=True),
    html.Div(
        className="mainContainer",
        children=[
            html.Div(
                html.Div(
                    children=[
                        html.Div(
                            className="pretty_container eight columns",
                            children=[
                                html.Br(),
                                html.Table(
                                    html.Tr(
                                        html.Th('Campus')
                                    ),
                                )
                            ]
                        ),
                        html.Div(
                            className="mini container",
                            children=[
                                html.Br(),
                                html.Button(id='back-button', children='Go back', n_clicks=0)
                            ]
                        )
                    ]
                ),
                className='row flex-display',
            )
        ]
    )
])


# Create callbacks
@app.callback(Output('url_login_df', 'pathname'),
              [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/utarDashboard'
