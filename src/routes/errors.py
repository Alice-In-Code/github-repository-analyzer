"""
Defines application-wide error handlers.

Handles HTTP errors and returns custom error pages for the given error.
"""

from flask import render_template
from flask.typing import ResponseReturnValue

from werkzeug.exceptions import (
    BadRequest,
    NotFound
)


# Error handlers

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
