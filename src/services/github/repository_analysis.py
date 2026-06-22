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
    get_repository_languages,
    get_user,
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

    owner = get_user(repository["owner"]["login"])

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

    languages = simplify_languages(
        get_repository_languages(
            repository_name
        )
    )

    return {
        "repository": repository,

        "owner": owner,

        "issues": {

            "open": open_issues,

            "closed": closed_issues
        },

        "pull_requests": {

            "open": open_prs,

            "closed": closed_prs
            },

        "repository_size": get_repository_size(repository),

        "languages": languages

        }


def simplify_languages(languages: dict[str, int]) -> dict[str, int]:
    """
    Simplify languages pie chart by labeling minimal languages "other".

    Args:
        languages:
            Dictionary of languages used in repository.

    Returns:
        Simplified dictionary of languages used in repository with their percent usage.
    """

    if not languages:
        return {}

    total = sum(languages.values())

    result = {}

    other = 0

    for language, bytes_count in languages.items():

        percentage = (
            bytes_count / total
        ) * 100

        if percentage < 1:
            other += bytes_count

        else:
            result[language] = bytes_count

    if other:
        result["Other"] = other

    return result
