"""
Repository analysis service.

Combines GitHub API data into a structure used by the application.
"""


from typing import Any


from src.services.github.repository_api import (
    get_repository,
    get_repository_items_count,
    get_pull_requests_count,
    get_repository_size,
)


def analyze_repository(repository_name: str) -> dict[str, Any] | None:
    """
    Retrieve and prepare repository analysis data.

    Args:
        repository_name:
            Name of the GitHub repository (owner/repository)

    Returns:
        Repository analysis data.
    """

    repository = get_repository(repository_name)

    if repository is None:
        return None

    open_issues = get_repository_items_count(
        repository_name,
        "open"
    )

    closed_issues = get_repository_items_count(
        repository_name,
        "closed"
    )

    open_prs = get_pull_requests_count(
        repository_name,
        "open"
    )

    closed_prs = get_pull_requests_count(
        repository_name,
        "closed"
    )

    return {
        "repository": repository,

        "issues": {

            "open": open_issues,

            "closed": closed_issues
        },

        "pull_requests": {

            "open": open_prs,

            "closed": closed_prs
            },

        "repository_size": get_repository_size(repository)

        }
