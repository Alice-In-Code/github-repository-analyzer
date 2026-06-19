"""
GitHub API service functions.

This module is responsible for communicating with the GitHub API.
"""

from typing import Any

import requests


BASE_URL = "https://api.github.com/repos"


def get_repository(repository_name: str) -> dict[str, Any] | None:
    """
    Fetch repository data from GitHub.

    Args:
        repository_name:
            Name of the GitHub repository (owner/repository).
        
    Returns:
        Repository data if found; otherwise None.
    """

    # Build the GitHub API endpoint URL.
    url = f"{BASE_URL}/{repository_name}"

    response = requests.get(url)

    # Return repository data when request succeeds
    if response.status_code == 200:
        return response.json()

    return None


def get_repository_items_count(
        repository_name: str,
        state: str
) -> int | str:
    """
    Fetch repository issue + pull request count.

    Args:
        repository_name:
            Name of the GitHub repository (owner/repository)

        state:
            If the issue is open or closed

    Returns:
        Number of repository issues if available, otherwise "N/A".
    """

    url = "https://api.github.com/search/issues"


    response = requests.get(
        url,
        params={
            "q": f"repo:{repository_name} is:issue state:{state}"
        }
    )

    if response.status_code != 200:
        return "N/A"

    return response.json()["total_count"]




def get_pull_requests_count(
        repository_name: str,
        state: str
) -> int | str:
    """
    Fetch repository pull request count

    Args:
        repository_name:
            Name of the GitHub repository (owner/repository).

        state:
            state:
               If the pull request is open or closed.

    Returns:
        Number of repository pull requests if available, otherwise "N/A".
    """

    url = f"{BASE_URL}/{repository_name}/pulls"

    response = requests.get(
        url,
        params={
            "state": state,
            "per_page": 1
        }
    )

    if response.status_code != 200:
        return "N/A"

    return get_total_paginated_count(response)


def get_total_paginated_count(response: requests.Response) -> int:
    """
    Extract total count from GitHub pagination headers.

    Args:
        response:
            Response to HTTP request.

    Returns:
        Pagination number if available, otherwise "N/A".
    """

    link_header = response.headers.get("Link")

    if not link_header:
        return len(response.json())

    for link in link_header.split(","):

        # Getting last page number (pagination number).
        if 'rel="last"' in link:

            url = link.split(";")[0].strip("<>")

            page_number = url.split("page=")[-1]

            return int(page_number)

    return len(response.json())


def get_repository_size(repository: dict[str, Any]) -> dict[str, int | float | str]:
    """
    Extract repository size in KB and transform it to KB, MB or GB depending on size if available, otherwise "N/A".

    Args:
        repository:
            Repository data.

    Returns:
        Repository size value and unit if available, otherwise "N/A".
    """
    # Fetch repository size in KB.
    size_kb = repository.get("size")


    # Checking if repository size is None.
    if not isinstance(size_kb, int):
        return {
            "value": 0,
            "unit": "N/A"
        }

    if size_kb < 1024:
        return {
            "value": size_kb,
            "unit": "KB"
        }

    # Calculate repository size in MB.
    size_mb = size_kb / 1024

    if size_mb < 1024:
        return {
            "value": round(size_mb),
            "unit": "MB"
        }

    # Calculate repository size in GB.
    size_gb = size_mb / 1024

    return {
        "value": round(size_gb, 2),
        "unit": "GB"
    }


