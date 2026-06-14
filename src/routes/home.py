"""
Routes for rendering the main application pages.

Includes the homepage and other static or entry-point views.
"""

from flask import (
    Blueprint,
    render_template,
)
from flask.typing import ResponseReturnValue

# Blueprints

home_blueprint = Blueprint(
    "home",
    __name__
)


# Routes

@home_blueprint.route("/")
def home() -> ResponseReturnValue:
    """
    Render the homepage.

    Returns:
        Rendered homepage template.
    """
    return render_template("index.html")
