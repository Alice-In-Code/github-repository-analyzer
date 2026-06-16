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

from src.services.github.repository_api import get_repository
from src.services.github.repository_input import parse_repository_input
from src.services.github.repository_normalizer import RepositoryNormalizationError

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

    repository_name = request.form.get("repository")

    if not repository_name:
        abort(
            400,
            description="Repository input is required."
        )

    try:
        repository_name = parse_repository_input(repository_name)

    except RepositoryNormalizationError as e:
        abort(400, description=str(e))

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
