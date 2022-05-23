# Dash packages
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import html, dcc


from app import app

# This is mock data representing small amounts of MOB sent out over the last 90 days
data = pd.read_csv("mob_sent_out.csv")

# This is a histogram of accumulation per user
mob_by_user = px.histogram(data, x="To User", y="Amount in USD")

# This is a line graph of accumulated MOB sent out over time
mob_over_time = px.line(
    data,
    x="Date",
    y=data["Amount in USD"].cumsum(),
)

# This is the big red button that stops the distribution of MOB
emergency_button = [
    dbc.CardHeader("Danger Zone"),
    dbc.CardBody(
        [
            html.H5("Emergency Stop", className="card-title"),
            html.P(
                "Pressing this button will immediately stop all MOB distribution. This cannot be undone.",
                className="card-text",
            ),
            dbc.Row(
                [
                    dbc.Col(),
                    dbc.Col(
                        dbc.Button(
                            "EMERGENCY STOP",
                            color="danger",
                            id="emergency-stop",
                            size="lg",
                        )
                    ),
                    dbc.Col(),
                ]
            ),
        ]
    ),
]


###############################################################################
########### LANDING PAGE LAYOUT ###########
###############################################################################
layout = dbc.Container(
    [
        html.H1("Magic MOB Mover Machine Analytics"),
        html.Hr(),
        html.H2("MOB Sent Out by User"),
        dbc.Row(
            children=[
                dcc.Graph(id="user-graph", figure=mob_by_user),
            ]
        ),
        html.H2("MOB Sent Out over time"),
        dbc.Row(
            children=[
                dcc.Graph(id="time-graph", figure=mob_over_time),
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    dbc.Card(emergency_button, color="danger", outline=True),
                ),
            ],
        ),
        dbc.Row(),
    ],
    className="mt-4",
)
