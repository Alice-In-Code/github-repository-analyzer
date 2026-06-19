"""
Automated tests for the GitHub API service.
"""

from unittest.mock import Mock, patch

from src.services.github.repository_api import (
    get_repository,
    get_repository_items_count,
    get_pull_requests_count
)


@patch("src.services.github.repository_api.requests.get")
def test_get_repository_success(mock_get: Mock) -> None:
    """Verify repository data is returned for a valid repository."""

    mock_response = Mock()

    mock_response.status_code = 200

    mock_response.json.return_value = {
        "name": "alice-in-code"
    }

    mock_get.return_value = mock_response

    repository = get_repository("alice-in-code/github-repository-analyzer")

    mock_get.assert_called_once_with("https://api.github.com/repos/alice-in-code/github-repository-analyzer")

    assert repository is not None
    assert repository["name"] == "alice-in-code"


@patch("src.services.github.repository_api.requests.get")
def test_get_repository_not_found(mock_get: Mock) -> None:
    """Verify None is returned for a missing repository."""

    mock_response = Mock()

    mock_response.status_code = 404

    mock_get.return_value = mock_response

    repository = get_repository("owner/repository")

    mock_get.assert_called_once_with("https://api.github.com/repos/owner/repository")

    assert repository is None


@patch("src.services.github.repository_api.requests.get")
def test_get_repository_items_count_success(mock_get: Mock) -> None:
    """
        Verify repository items count is successful.

        Args:
            mock_get:
                Mock object used to verify the external call successfully returns items count.
    """

    response = Mock()

    response.status_code = 200

    response.json.return_value = {
        "total_count": 0
    }

    mock_get.return_value = response

    result = get_repository_items_count(
        "owner/repository",
        "closed"
    )

    mock_get.assert_called_once()

    assert result == 0


@patch("src.services.github.repository_api.requests.get")
def test_get_pull_requests_count_success(mock_get: Mock) -> None:
    """
        Verify repository items count is successful.

        Args:
            mock_get:
                Mock object used to verify the external call successfully returns pull request count.
    """

    response = Mock()

    response.status_code = 200

    response.headers = {}

    response.json.return_value = [
        {},
        {}
    ]

    mock_get.return_value = response

    result = get_pull_requests_count(
        "owner/repository",
        "open"
    )

    assert result == 2
