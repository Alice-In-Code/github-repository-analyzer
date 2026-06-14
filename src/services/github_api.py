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
        repository_name: Name of the GitHub repository (owner/repository).
        
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
