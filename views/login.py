import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from server import app, User
from flask_login import login_user
from werkzeug.security import check_password_hash

layout = html.Div(
    className="limiter",
    children=[
        html.Div(
            [
                html.Div(
                    className="wrap-login100 p-t-30 p-b-50",
                    children=[
                        dcc.Location(id='url_login', refresh=True),
                        html.Span('''Dashboard Login''', className='login100-form-title p-b-41'),
                        html.Form(
                            # method='Post',
                            children=[
                                html.Div(
                                    [
                                        dcc.Input(
                                            placeholder='Username',
                                            type='text',
                                            id='uname-box',
                                            className='input100'
                                        ),
                                        html.Span(className='focus-input100'),
                                    ],
                                    className='wrap-input100'
                                ),

                                html.Div(
                                    [
                                        dcc.Input(
                                            placeholder='Password',
                                            type='password',
                                            id='pwd-box',
                                            className='input100'
                                        ),
                                        html.Span(className='focus-input100'),
                                    ],
                                    className='wrap-input100'
                                ),
                                html.Div(
                                    html.Button(
                                        children='Login',
                                        n_clicks=0,
                                        type='submit',
                                        id='login-button',
                                        className='login100-form-btn'
                                    ),
                                    className='container-login100-form-btn m-t-32'
                                ),
                                html.Div(children='', id='output-state')
                            ],
                        className="login100-form p-b-33 p-t-5",
                        ),
                    ]
                )
            ],
            className="container-login100",
        )
    ]
)


@app.callback(Output('url_login', 'pathname'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def sucess(n_clicks, input1, input2):
    user = User.query.filter_by(username=input1).first()
    if user:
        if check_password_hash(user.password, input2):
            login_user(user)
            return '/utarDashboard'
        else:
            pass
    else:
        pass


@app.callback(Output('output-state', 'children'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def update_output(n_clicks, input1, input2):
    if n_clicks > 0:
        user = User.query.filter_by(username=input1).first()
        if user:
            if check_password_hash(user.password, input2):
                return ''
            else:
                return 'Incorrect username or password'
        else:
            return 'Incorrect username or password'
    else:
        return ''