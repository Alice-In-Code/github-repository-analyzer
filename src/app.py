"""
Application entry point for the GitHub Repository Analyzer.
"""

from flask import Flask, render_template, request, abort
from flask.typing import ResponseReturnValue

from src.services.github_api import get_repository

app = Flask(__name__)


@app.route("/")
def home() -> str:
    """
    Render the homepage.

    Returns:
        Rendered homepage template.
    """
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
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


if __name__ == "__main__":
    app.run(debug=True)
