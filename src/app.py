"""
Application entry point for the GitHub Repository Analyzer.
"""

from flask import Flask

from werkzeug.exceptions import BadRequest, NotFound

from src.routes.errors import handle_bad_request, handle_not_found
from src.routes.home import home_blueprint
from src.routes.analyze import analyze_blueprint

app = Flask(__name__)


# Register route blueprints.

app.register_blueprint(home_blueprint) # Home blueprint
app.register_blueprint(analyze_blueprint) # Analyze blueprint


# Register application error handlers.

app.register_error_handler(
    BadRequest,
    handle_bad_request
)

app.register_error_handler(
    NotFound,
    handle_not_found
)


if __name__ == "__main__":
    app.run(debug=True)
