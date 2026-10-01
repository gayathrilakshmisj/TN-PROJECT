"""Route blueprints package."""
from flask import Blueprint

home_bp = Blueprint("home", __name__)
party_bp = Blueprint("party", __name__)
jewelry_bp = Blueprint("jewelry", __name__)

from routes import home_routes, party_routes, jewelry_routes
