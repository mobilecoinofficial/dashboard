# Dash packages
import dash_bootstrap_components as dbc
from dash import html

from app import app

###############################################################################
########### PAGE 2 LAYOUT ###########
###############################################################################
layout = dbc.Container(
    [
        html.H2("Page 2 Layout"),
        html.Hr(),
    ],
    className="mt-4",
)
