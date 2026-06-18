"""
Application entry point for the GitHub Repository Analyzer.
"""

from flask import Flask

from werkzeug.exceptions import HTTPException

from src.routes.errors import (
    handle_http_error,
    handle_internal_error
)
from src.routes.home import home_blueprint
from src.routes.analyze import analyze_blueprint


def register_blueprints(app: Flask) -> None:
    """Register application route blueprints."""

    app.register_blueprint(home_blueprint)
    app.register_blueprint(analyze_blueprint)


def register_error_handlers(app: Flask) -> None:
    """Register application error handlers."""

    app.register_error_handler(
        HTTPException,
        handle_http_error
    )

    app.register_error_handler(
        Exception,
        handle_internal_error
    )


def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
         Configured Flask application instance.
    """

    app = Flask(__name__)

    register_blueprints(app)
    register_error_handlers(app)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
