"""
Defines application-wide error handlers.

Handles HTTP errors and returns custom error pages for the given error.
"""
from flask import render_template
from flask.typing import ResponseReturnValue

from werkzeug.exceptions import HTTPException


# Error handler

def handle_http_error(error: HTTPException) -> ResponseReturnValue:
    """
    Handles HTTP errors and renders error template.

    Args:
        error:
            Raised Flask exception.

    Returns:
        Rendered error template.
    """

    status_code = error.code

    if status_code is None:
        status_code = 500

    return (
        render_template(
            "errors/error.html",
            error_code=status_code,
            error_title=error.name,
            error_description=error.description
        ),
        status_code
    )


def handle_internal_error(_error: Exception) -> ResponseReturnValue:
    """
    Handles unexpected application exception and renders error template.

    Args:
        _error:
            Unexpected application exception.

    Returns:
        Rendered error template.
    """

    ERROR_CODE = 500

    return (
        render_template(
            "errors/error.html",
            error_code=ERROR_CODE,
            error_title="Internal Server Error",
            error_description="An unexpected error occurred."
        ),
        ERROR_CODE
    )
