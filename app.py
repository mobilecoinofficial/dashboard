# Dash app initialization
import dash
import dash_bootstrap_components as dbc

# User management initialization
import os
from flask_login import LoginManager, UserMixin
from users_mgt import db, User as base
from config import config


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUMEN],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app.config.suppress_callback_exceptions = True


# config
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=config.get("database", "con"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db.init_app(server)

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"

# Create User class with UserMixin
class User(UserMixin, base):
    pass


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
