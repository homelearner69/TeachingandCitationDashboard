import warnings
# Dash configuration
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from datetime import datetime as dt
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import base64
plt.style.use('fivethirtyeight')

from server import app

warnings.filterwarnings("ignore")

df = pd.read_json("https://raw.githubusercontent.com/homelearner69/Brian/master/studentFeedback.json")
newdf = df[['StudentFeedback','Polarity']]


formatSub = df['Subjectivity'].mean()
averageSub= "{:.2f}".format(formatSub)


formatPol = df['Polarity'].mean()
averagePol= "{:.2f}".format(formatPol)

pFeedbacks = df[df.TextAnalysis == 'Positive']
pFeedbacks = pFeedbacks['StudentFeedback']
percentPFeedback= str(round((pFeedbacks.shape[0] / df.shape[0]) * 100,1))


NFeedbacks = df[df.TextAnalysis == 'Negative']
NFeedbacks = NFeedbacks['StudentFeedback']
percentNFeedback = str(round((NFeedbacks.shape[0] / df.shape[0]) * 100,1))

NeuFeedbacks = df[df.TextAnalysis == 'Neutral']
NeuFeedbacks = NeuFeedbacks['StudentFeedback']
percentNeuFeedback = str(round((NeuFeedbacks.shape[0] / df.shape[0]) * 100,1))

sentAnalysisChart = px.scatter(df, y='Subjectivity', x='Polarity',color='TextAnalysis', title = 'Sentiment Analysis of Teaching Survey')

x = df['TextAnalysis'].value_counts()
y=df['TextAnalysis'].unique()
sentimentCount = px.bar(df, y=y, x=x, labels={'x':'Counts','y':'Nature'} ,title = 'Nature of student feedback')


allWords = ' '.join([feedback for feedback in df['StudentFeedback']])
wordCloud =  WordCloud(width = 1000, height = 600, random_state=21 , max_font_size = 119).generate(allWords)

plt.imshow(wordCloud, interpolation ='bilinear')
plt.axis('off')
cloudFigure = plt.axis('off')
# Create success layout
layout = html.Div(
    [
        dcc.Location(id='url_dashboard', refresh=True),
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Filter by Date :",
                            className="control_label",
                        ),
                        dcc.DatePickerRange(
                            id='my-date-picker-range',
                            min_date_allowed=dt(2019, 8, 5),
                            max_date_allowed=dt(2021, 9, 19),
                            initial_visible_month=dt(2020, 8, 5),
                            end_date=dt(2020, 10, 25).date(),
                            className="dcc_control",
                        ),
                        html.P(
                            "Filter by Sentiment :",
                            className="control_label",
                        ),
                        dcc.Checklist(
                            id="category_selector",
                            options=[
                                {"label": "Positive", "value": "Positive"},
                                {"label": "Neutral", "value": "Neutral"},
                                {"label": "Negative ", "value": "Negative"},
                            ],
                            value="Positive",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H5(averageSub), html.P("Average Review Subjectivity")],
                                    id="citations",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H5(averagePol), html.P("Average Review Polarity")],
                                    id="staffs",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H5(percentPFeedback + "%"), html.P("Percentage of Positive Feedback")],
                                    id="h-index",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H5(percentNFeedback + "%"), html.P("Number of Negative Feedback")],
                                    id="document",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H5(percentNeuFeedback + "%"), html.P("Number of Neutral Feedback")],
                                    id="document",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
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
                     [html.H5('WordCloud of Dr.Pradeep Student Survey'),
                      html.Img(id="image_wc")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="sentimentCount",figure = sentimentCount)],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="sentimentGraph", figure = sentAnalysisChart)],
                    className="pretty_container seven columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


def plot_wordcloud(data):
    allWords = ' '.join([feedback for feedback in df['StudentFeedback']])
    wc = WordCloud(background_color='black', width=700, height=400, random_state=21 , max_font_size = 119).generate(allWords)
    return wc.to_image()

@app.callback(Output('image_wc', 'src'), [Input('image_wc', 'id')])
def make_image(b):
    img = BytesIO()
    plot_wordcloud(data=newdf).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
