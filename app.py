# index page
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_table

from flask import Flask
from server import app, server
from flask_login import logout_user, current_user, LoginManager
from views import login, sentiment, logout
from controls import COUNTIES, FACULTY, DEPARTMENT, DEPARTMENT_COLORS


faculty_options = [
    {"label": str(FACULTY[fac]), "value": str(fac)}
    for fac in FACULTY
]

all_options = {
    'kpr': ['FAS', 'FBF', 'FICT','FEGT','FSc','CFSKPR','ICSKPR'],
    'sgl': ['FAM', 'FMHS', 'FCI','LKCFES','CFSSGL','ICSSGL'],
    'all': [],
    'ctm':[]
}

department_options = [
    {"label": str(DEPARTMENT[dep]), "value": str(dep)}
    for dep in DEPARTMENT
]


#Department data for the teaching survey data
departmentData = pd.read_json("https://raw.githubusercontent.com/homelearner69/Brian/master/departmentData.json")
departmentData = departmentData.rename(columns = {"document-count" : "DocumentCount","citations-count": "TotalCitations", "cited-by-count" : "CitedbyCount", "coauthor-count" : "CoAuthorCount", "surname" : "LastName", "given-name" : "FirstName", "h-index": "HIndex" })


#Publication Data for citations monitoring
df = pd.read_csv("https://raw.githubusercontent.com/homelearner69/Brian/master/mainAuthorDataCleaned.csv")
dataFrame = df.rename(columns = {"document-count" : "DocumentCount","citations-count": "TotalCitations", "cited-by-count" : "CitedbyCount", "coauthor-count" : "CoAuthorCount", "surname" : "LastName", "given-name" : "FirstName", "h-index": "HIndex" })
dataFrame= dataFrame.drop(['affiliation-name'],axis=1)

formatCitations = dataFrame['TotalCitations'].mean()
averageCitation = "{:.2f}".format(formatCitations)
totalStaff = str(dataFrame['LastName'].count())

formatIndex = dataFrame['HIndex'].max()
highestIndex = "{:.2f}".format(formatIndex)

formatDocument = dataFrame['DocumentCount'].mean()
totalDocument = "{:.2f}".format(formatDocument)

modal = html.Div(
    [
        dbc.Button("What is 'DCS'?", id="open"),
        dbc.Modal(
            [
                dbc.ModalHeader("Department Abbreviation"),
                dbc.ModalBody(id='departmentData'),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id='modal',
            className='pretty_container four columns',
        ),
    ]
)

header = html.Div(
    className='header',
    children=html.Div(
        className='container-width',
        style={'height': '100%'},
        children=[
            html.A([
                html.Img(
                    src='assets/utar.png',
                    className='logo'
                ),
            ], href='/utarDashboard'),
            html.P(
                "Universiti Tunku Abdul Rahman",
                className='utartext'
            ),
            html.Div(className='links', children=[
                html.Div(id='sentiment', className='link'),
                html.Div(id='user-name', className='link'),
                html.Div(id='logout', className='link')
            ])
        ]
    )
)

#Main layout
app.layout = html.Div(
    [
        header,
        html.Div([
            html.Div(
                html.Div(id='page-content', className='content'),
                className='row flex-display'
            ),
        ], className="mainContainer",),
        dcc.Location(id='url', refresh=False),
    ]
)

#The dashboard layout
dashboard_layout = html.Div(
    [
        dcc.Location(id='url_dashboard', refresh=True),
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(id="myInfo"),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Filter by Category :",
                            className="control_label",
                        ),
                        dcc.RadioItems(
                            id="category_selector",
                            options=[
                                {"label": "Document Count", "value": "DocumentCount"},
                                {"label": "Total Citations", "value": "TotalCitations"},
                                {"label": "Cited By Count ", "value": "CitedbyCount"},
                                {"label": "H-Index", "value": "HIndex"},
                                {"label": "Co-Author Count", "value": "CoAuthorCount"},
                            ],
                            value="TotalCitations",
                            labelStyle={"display": "inline-block","color":"#FFFFFF"},
                            className="dcc_control",
                        ),
                        html.P("Filter by faculty:",
                               className="control_label"),
                         dcc.RadioItems(
                            id="faculty_selector",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "Kampar", "value": "kpr"},
                                {"label": "Sungai Long", "value": "sgl"},
                                {"label": "Customise", "value": "ctm"},
                            ],
                            value="kpr",
                            labelStyle={"display": "inline-block","color":"#FFFFFF"},
                            className="dcc_control",
                        ),
                         dcc.Dropdown(
                            id="faculty_types",
                            options=faculty_options,
                            multi=True,
                            value=list(FACULTY.keys()),
                            className="dcc_control",
                        ),
                        dcc.Checklist(
                            id="lock_selector",
                            className="dcc_control",
                            value=[],
                        ),
                        html.P("Filter by Department:",
                               className="control_label"),
                         dcc.RadioItems(
                            id="department_selector",
                            labelStyle={"display": "inline-block","color":"#FFFFFF"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="department_types",
                            multi=True,
                            options=department_options,
                            value=list(DEPARTMENT.keys()),
                            className="dcc_control",
                        ),
                        html.Div(modal),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H5(averageCitation), html.P("UTAR Average Citations")],
                                    id="citations",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H5(totalStaff), html.P("UTAR Total Staffs")],
                                    id="staffs",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H5(highestIndex), html.P("UTAR Highest H-Index")],
                                    id="h-index",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H5(totalDocument), html.P("UTAR Average Publications")],
                                    id="document",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            children=[
                                html.Div(id="tableTitle", className="subtitle"),
                                html.Div(id="top_open_opportunities", className="table"),
                        ],
                            id="countGraphContainer",
                            className="pretty_container seven columns",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                     [dcc.Graph(id="facNameGraph")],
                    className="pretty_container twelve columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="depNameGraph")],
                    className="pretty_container twelve columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="departmentGraph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="facultyGraph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="pie_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

#Callback to control the modal for DCS
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Helper functions
def human_format(num):
    if num == 0:
        return "0"

    magnitude = int(math.log(num, 1000))
    mantissa = str(int(num / (1000 ** magnitude)))
    return mantissa + ["", "K", "M", "G", "T", "P"][magnitude]

#Filters applying to the selectors
def filter_dataframe(dataFrame, faculty, department):
    dff = dataFrame[
        dataFrame.department.isin(department) &
        dataFrame.faculty.isin(faculty)
    ]
    return dff

def filter_facDataFrame(dataFrame, faculty):
    dfff = dataFrame[
        dataFrame.faculty.isin(faculty)
    ]
    return dfff

def filter_depDataFrame(dataFrame, department):
    dfff = dataFrame[
        dataFrame.department.isin(department)
    ]
    return dfff

#Data table beside the filter
def df_to_table(dff):
    return html.Table(
        [html.Tr([html.Th(col) for col in dff.columns])]
        + [
            html.Tr([html.Td(dff.iloc[i][col]) for col in dff.columns])
            for i in range(len(dff))
        ]
    )

def infoData_to_table(dff):
    return html.Table(
        [html.Tr([html.Th(col) for col in dff.columns])]
        + [
            html.Tr([html.Td(dff.iloc[i][col]) for col in dff.columns])
            for i in range(len(dff))
        ]
    )
    
@app.callback(
    Output("departmentData", "children"),
    [
        Input("category_selector", "value")
    ], 
)
def top_departmentData(category):
    dff = departmentData.sort_values(category, ascending=False)
    cols = ["Abbreviation", "Department", "Faculty"]
    dfff = dff[cols].iloc[:60]
    # only display 21 characters
    dfff["Department"] = dfff["Department"].apply(lambda x: x[:30])
    return infoData_to_table(dfff)

@app.callback(
    Output("top_open_opportunities", "children"),
    [
        Input("category_selector", "value")
    ],
)
def top_open_opportunities(category):
    dff = dataFrame.sort_values(category, ascending=False)
    cols = ["LastName","FirstName", category , "faculty", "department"]
    dfff = dff[cols].iloc[:6]
    # only display 21 characters
    dfff["FirstName"] = dfff["FirstName"].apply(lambda x: x[:30])
    return df_to_table(dfff)

@app.callback(
    Output("tableTitle", "children"),
    [
        Input("category_selector", "value")
    ],
)
def change_table_title(category):
    titleTable = str(category)
    return html.H6("Top " + category + " Lecturers")

# Radio -> multi
@app.callback(
    Output("faculty_types", "value"), [Input("faculty_selector", "value")]
)
def display_status(selector):
    if selector == "all":
        return list(FACULTY.keys())
    elif selector == "kpr":
        return ["FAS","FBF","FEGT","FICT","FSc","CFSKPR","ICSKPR"]
    elif selector == "sgl":
        return ["FAM","FMHS","FCI","LKCFES","CFSSGL","ICSSGL"]
    elif selector == "ctm":
        return []
    return []

@app.callback(
    Output('department_selector', 'options'),
    [Input('faculty_selector', 'value')])
def set_department_options(selected_campus):
    return [{'label': i, 'value': i} for i in all_options[selected_campus]]

#Radio -> multi
@app.callback(Output("department_types", "value"), [Input("department_selector", "value")])
def display_type(faculty_types):
    if faculty_types == "FAM":
        return ["DOA","DBPM","DOE","DIB"]
    elif faculty_types == "FAS":
        return ["DOAD", "DOJ", "DOLL", "DOPC", "DPR"]
    elif faculty_types == "FICT":
        return ["DCS", "DCCT", "DIS"]    
    elif faculty_types == "FBF":
        return ["DOB", "DOCA", "DE", "DOEN", "DOF","DOM"]
    elif faculty_types == "FCI":
        return ["DOAD", "DGEN", "DMC", "DM", "DMDA"]
    elif faculty_types == "FEGT":
        return ["DCM", "DEE", "DEV", "DIE", "DPCE"]
    elif faculty_types == "FMHS":
        return ["DCMED", "DMED", "DON", "DOP", "DOPM","DPCS"]
    elif faculty_types == "FSc":
        return ["DAFS", "DAHS", "DBS", "DCHS", "DPMS"]
    elif faculty_types == "LKCFES":
        return ["DASD", "DCE", "DEEE", "DIECS", "DMAS","DMME","DMBE","DOS"]
    elif faculty_types == "CFSKPR":
        return ["DMA", "DSEKPR"]
    elif faculty_types == "CFSSGL":
        return ["DSESGL"]                                          
    return []


#this callback controls the department lecturer graph
@app.callback(
    Output("depNameGraph", "figure"),
    [
        Input("department_types","value"),
        Input("category_selector", "value")
    ],
)
def plot_main_figure(department, category):

    dff = filter_depDataFrame(dataFrame, department)
    depColour = dataFrame['department'].unique()

    x = dff['FirstName']
    y = dff[category]

    data = dict(
        type="bar",
        name=category,
        x=x,
        y=y,
        xaxis='FirstName'
    ),


    layout = dict(
        title= "Academic Staff {} by <br> {} <br> Department".format(category,department),
        plot_bgcolor="#E5ECF6",
        paper_bgcolor="#F9F9F9",
        hoverinfo= "x+y",
        hovertext="FirstName",
        textinfo="x+y",
        autosize=True,
        animate=True,
        automargin=True
    )
    # layout = dict(
    #     autosize=True,
    #     barmode="stack",
    #     automargin=True,
    #     paper_bgcolor="white",
    #     plot_bgcolor="white",
    # )


    figure = dict(data=data, layout=layout)
    return figure

#this callback controls the faculty lecturer graph
@app.callback(
    Output("facNameGraph", "figure"),
    [
        Input("faculty_types", "value"),
        Input("category_selector", "value")
    ],
)
def plot_main_figure(faculty,category):

    dff = filter_facDataFrame(dataFrame, faculty)
    depColour = dataFrame['department'].unique()

    x = dff['FirstName']
    y = dff[category]

    data = dict(
        type="bar",
        name=category,
        x=x,
        y=y,
        xaxis='FirstName'
    ),


    layout = dict(
        title= "Academic Staff {} by <br> {} <br> Faculty".format(category,faculty),
        plot_bgcolor="#E5ECF6",
        paper_bgcolor="#F9F9F9",
        hoverinfo= "x+y",
        hovertext="FirstName",
        textinfo="x+y",
        autosize=True,
        animate=True,
        automargin=True
    )


    figure = dict(data=data, layout=layout)
    return figure

#Selectors -> faculty graph
#this callback controls the faculty average graph
@app.callback(
    Output("facultyGraph", "figure"),
    [
        Input("faculty_types", "value"),
        Input("category_selector", "value")
    ],
)
def plot_faculty_figure(faculty,category):
    color = dataFrame['department'].unique()

    dff = filter_facDataFrame(dataFrame, faculty)
    
    #df = df.groupby(['faculty'])[category].mean()
        
    
    x = dff['faculty'].unique()
    y = dff.groupby(['faculty'])[category].mean()

    data = dict(
        type="bar",
        name=category,
        barmode="group", 
        color=color,
        x=x,
        y=y,
        hoverinfo="name+x+y",
        hovertext="name",
        textinfo="x+y",
        marker=dict(line= dict(colors=["#92d8d8","#fac1b7"])),
        textposition="inside"
    ),


    layout = dict(
        title= "Average {} by <br> {} <br> Faculty".format(category,faculty),
        plot_bgcolor="#E5ECF6",
        paper_bgcolor="#F9F9F9",
        autosize=True,
        automargin=True
    )


    figure = dict(data=data, layout=layout)
    return figure

#Selectors -> faculty graph
#this callback controls the department average graph
@app.callback(
    Output("departmentGraph", "figure"),
    [
        Input("department_types", "value"),
        Input("category_selector", "value")
    ],
)
def plot_department_figure(department,category):
    color = dataFrame['department'].unique()

    dff = filter_depDataFrame(dataFrame, department)  
    
    x = dff['department'].unique()
    y = dff.groupby(['department'])[category].mean()

    data = dict(
        type="bar",
        name=category,
        barmode="group",
        color=color,
        x=x,
        y=y,
        hoverinfo="name+x+y",
        hovertext="name",
        textinfo="x+y",
        textposition="inside"
    ),

    layout = dict(
        title= "Average {} by <br> {} <br> Department".format(category,department),
        plot_bgcolor="#E5ECF6",
        paper_bgcolor="#F9F9F9",
        autosize=True,
        automargin=True
    )

    figure = dict(data=data, layout=layout)
    return figure

#this callback controls the gender based on the faculty pie chart
@app.callback(
    Output("pie_graph", "figure"),
    [
        Input("faculty_types", "value"),
        Input("faculty_selector","value")
    ],
)
def plot_main_figure(faculty, facselect):

    dfff = filter_facDataFrame(dataFrame, faculty)
    
    preFacMale = dfff.loc[(df['gender'] == 'male')]
    preFacFemale = dfff.loc[(df['gender'] == 'female')]

    facMale = preFacMale['gender'].count()
    facFemale = preFacFemale['gender'].count()
    
    
    data = [
        dict(
        type="pie",
        values=[facMale, facFemale],
        labels=["Male","Female"],
        name="Gender Composition",
        text=[
            "Male",
            "Female"
        ],
        hoverinfo="text+value",
        textinfo="label+percent+name",
        hole=0.5,
        marker=dict(colors=["#92d8d8","#fac1b7"]),
        domain={"x": [0, 1], "y": [0.2, 0.8]},
        ),
    ]
    
    layout = dict(
        title= "Gender Composition of <br> {} <br> Faculty".format(faculty),
        font= dict(color='#777777'),
        legend=dict(font=dict(color="#CCCCCC", size="10"), orientation="h", bgcolor="rgba(0,0,0,0)"),
        plot_bgcolor="#E5ECF6",
        paper_bgcolor="#F9F9F9",
        autosize=True,
        automargin=True
    )

    figure = dict(data=data, layout=layout)
    return figure        


#this callback controls the webpage to display which layout 
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return login.layout
    elif pathname == '/login':
        return login.layout
    elif pathname == '/utarDashboard':
        if current_user.is_authenticated:
            return dashboard_layout
        else:
            logout_user()
            return login.layout
    elif pathname == '/sentiment':
        return sentiment.layout
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return login.layout
        else:
            return login.layout
    else:
        return '404'

#this callback checks whether it is logged in
@app.callback(
    Output('user-name', 'children'),
    [Input('page-content', 'children')])
def cur_user(input1):
    if current_user.is_authenticated:
        return html.Div('Current user: ' + current_user.username)
        # 'User authenticated' return username in get_id()
    else:
        return ''


@app.callback(
    Output('logout', 'children'),
    [Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        return html.A('Logout', href='/logout')
    else:
        return ''
    
    
@app.callback(
    Output('sentiment', 'children'),
    [Input('page-content', 'children')])
def sentiment_page(input1):
    if current_user.is_authenticated:
        return html.A('Teaching Survey', href='/sentiment')
    else:
        return html.H3('Utar Staff Dashboard')


if __name__ == '__main__':
    app.run_server(debug=True)
