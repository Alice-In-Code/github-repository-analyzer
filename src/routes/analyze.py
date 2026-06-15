"""
Routes for repository analysis.

Handles user-submitted forms to retrieve repository data and render results using data from the GitHub API service.
"""

from flask import (
    Blueprint,
    abort,
    render_template,
    request
)
from flask.typing import ResponseReturnValue

from services.github.repository_api import get_repository


# Blueprints

analyze_blueprint = Blueprint("analyze", __name__)


# Routes

@analyze_blueprint.route("/analyze", methods=["POST"])
def analyze() -> ResponseReturnValue:
    """
    Retrieve repository information and display results.

    Returns:
        Rendered results page.
    """

    repository_name = request.form.get("repository", "").strip()

    if not repository_name:
        abort(
            400,
            description="Invalid repository name."
        )

    repository = get_repository(repository_name)

    if repository is None:
        abort(
            404,
            description=f'Repository "{repository_name}" could not be found.'
        )

    return render_template(
        "results.html",
        repository=repository
    )
