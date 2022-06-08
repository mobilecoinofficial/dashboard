import logging
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
from zero import ZeroClient

from config import config

# This is mock data representing small amounts of MOB sent out over the last 90 days
# data = pd.read_csv("mob_sent_out.csv")

# Make a zero client and use it to call the ledger API
client = ZeroClient("0.0.0.0", 5559)
# records = False
# if not records:
records = client.call("call_ledger_method", "get_all_txs")
data = pd.DataFrame(records)
data["amount_usd"] = data["amount_usd_cents"] / 100
data["amount_mob"] = data["amount_pmob"] / 1e12
logging.info(data)

# This is a histogram of accumulation per user
user_payouts = go.Figure()
user_payouts.add_trace(
    go.Histogram(x=data["account"], y=data["amount_usd"], histfunc="sum")
)
user_payouts.add_trace(
    go.Histogram(x=data["account"], y=data["amount_mob"], histfunc="sum")
)
user_payouts.update_layout(barmode="overlay")
user_payouts.update_traces(opacity=0.7)

# Get a the mob_

# This is a line graph of accumulated MOB sent out over time
payouts_over_time = px.line(data, x="ts", y=data["amount_usd"].cumsum())

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
        html.H2("MOB sent to each user"),
        dbc.Row(
            children=[
                dcc.Graph(id="user-graph", figure=user_payouts),
            ]
        ),
        html.H2("Total USD value sent out over time"),
        dbc.Row(
            children=[
                dcc.Graph(id="time-graph", figure=payouts_over_time),
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    dbc.Card(emergency_button, color="danger", outline=True),
                ),
            ],
        ),
        html.Hr(),
        dbc.Row(),
    ],
    className="mt-4",
)
