"""
Application entry point for the GitHub Repository Analyzer.
"""

from flask import (
    Flask,
    render_template,
    request,
    abort
)
from flask.typing import ResponseReturnValue

from werkzeug.exceptions import BadRequest, NotFound

from src.services.github_api import get_repository

from src.routes.home import home_blueprint
from src.routes.analyze import analyze_blueprint

app = Flask(__name__)


# Register route blueprints.

app.register_blueprint(home_blueprint) # Home blueprint
app.register_blueprint(analyze_blueprint) # Analyze blueprint


# Error handlers

@app.errorhandler(BadRequest)
def handle_bad_request(error: BadRequest) -> ResponseReturnValue:
    """
    Render the bad request page.

    Args:
        error:
            Raised Flask exception.

    Returns:
        Rendered 400 error page.
    """

    return (
        render_template(
            "errors/400.html",
            error_description=error.description
        ),
        400
    )


@app.errorhandler(NotFound)
def handle_not_found(error: NotFound) -> ResponseReturnValue:
    """
    Render the not found page.

    Args:
        error:
            Raised Flask exception.

    Return:
        Rendered 404 error page.
    """

    return (
        render_template(
            "errors/404.html",
            error_description=error.description
        ),
        404
    )


if __name__ == "__main__":
    app.run(debug=True)
