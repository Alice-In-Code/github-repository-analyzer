"""
Automated tests for application routes.
"""



from unittest.mock import patch

import pytest

from src.app import create_app


def mock_analysis_result():
    """
    Helper function which returns mock repository analysis results used for test inputs.

    Returns:
        Mock analysis repository results.
    """
    return {
        "repository": {
            "name": "repository",
            "full_name": "owner/repository",
            "description": "Test repository",

            "default_branch": "main",

            "created_at": "0000-00-00T00:00:00Z",
            "pushed_at": "0000-00-00T00:00:00Z",
            "updated_at": "0000-00-00t00:00:00Z",

            "size": 0,

            "archived": False,

            "license": None,

            "stargazers_count": 0,
            "subscribers_count": 0,
            "forks_count": 0,

            "owner": {
                "login": "owner",
                "avatar_url": ""
            }
        },

        "owner": {
            "login": "owner",
            "name": "Owner Name",
            "bio": "Test owner bio",
            "avatar_url": "GitHub avatar URL",
            "followers": 0,
            "following": 0,
            "public_repos": 0,
        },

        "issues": {
            "open": 0,
            "closed": 0
        },

        "pull_requests": {
            "open": 0,
            "closed": 0
        },

        "repository_size": {
            "value": 0,
            "unit": "KB"
        },

        "languages": {
            "Python": 0,
            "HTML": 0,
            "CSS": 0
        }
    }



def test_homepage_loads() -> None:
    """
    Verify homepage loads successfully.
    """

    app = create_app()

    with app.test_client() as client:
        response = client.get("/")

    assert response.status_code == 200


@patch("src.routes.analyze.analyze_repository")
def test_repository_not_found_returns_404(mock_analyze) -> None:
    """
    Verify missing repositories return a 404 response.

    Args:
        mock_analyze:
            Mock object used to verify the external call returns 404 response.

    """

    mock_analyze.return_value = None

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/analyze",
            data={
                "repository": "owner/repository"
            }
        )

    assert response.status_code == 404
    assert b"could not be found" in response.data


@pytest.mark.parametrize(
    "repository_input",
    [
        "",
        " ",
    ]
)
def test_missing_repository_input_returns_400(repository_input: str) -> None:
    """
    Verify empty repository input returns a 400 response.

    Args:
        repository_input:
            List of empty and whitespaces for repository input.
    """

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/analyze",
            data={
                "repository": repository_input
            }
        )

    assert response.status_code == 400
    assert b"Repository input is required" in response.data


def test_invalid_repository_input_returns_400() -> None:
    """Verify invalid repository format returns a 400 response."""

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/analyze",
            data={
                "repository": "."
            }
        )

    assert response.status_code == 400
    assert b"Invalid repository format" in response.data


@pytest.mark.parametrize(
    "repository_input",
    [
        "https://github.com/owner/repository",
        "http://github.com/owner/repository",
        "github.com/owner/repository",
        "www.github.com/owner/repository",
    ]
)
@patch("src.routes.analyze.analyze_repository")
def test_github_url_input_is_normalized(
        mock_analyze,
        repository_input: str
) -> None:
    """
    Verify GitHub repository URL inputs are normalized before API request.

    Args:
        mock_analyze:
            Mock object used to verify the external analysis call is made with the expected normalized input.

        repository_input:
            List of non-normalized GitHub links for repository input.
    """

    mock_analyze.return_value = mock_analysis_result()

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/analyze",
            data={
                "repository": repository_input
            }
        )

    assert response.status_code == 200

    mock_analyze.assert_called_once_with(
        "owner/repository"
    )


@pytest.mark.parametrize(
    "repository_input",
    [
        "https://github.com",
        "https://github.com/",

        "http://github.com",
        "http://github.com/",

        "github.com",
        "github.com/",

        "www.github.com",
        "www.github.com/",
    ]
)
def test_github_url_without_repository_400(repository_input: str) -> None:
    """
    Verify incomplete GitHub repository URLs return 400 Error.

    Args:
        repository_input:
            List of GitHub URLs without repositories for repository input.
    """

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/analyze",
            data={
                "repository": repository_input
            }
        )

    assert response.status_code == 400


@patch("src.routes.analyze.analyze_repository")
def test_owner_repository_input_returns_200(mock_analyze) -> None:
    """
    Verify 'owner/repository' input is accepted and returns 200.

    Args:
        mock_analyze:
            Mock object used to verify the external call returns 200 response.
    """

    mock_analyze.return_value = mock_analysis_result()

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/analyze",
            data={
                "repository": "owner/repository"
            }
        )

    assert response.status_code == 200

    mock_analyze.assert_called_once_with(
        "owner/repository"
    )


@patch("src.routes.analyze.analyze_repository")
def test_owner_panel_renders_owner_information(mock_analyze) -> None:
    """
    Verify owner information is rendered in the owner panel.

    Args:
        mock_analyze:
            Mock object used to verify the external call returns repository owner information.
    """

    mock_analyze.return_value = mock_analysis_result()

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/analyze",
            data={
                "repository": "owner/repository"
            }
        )

    assert response.status_code == 200

    # Owner identity
    assert b"Owner Name" in response.data
    assert b"Test owner bio" in response.data

    # Owner stats
    assert b"Followers" in response.data
    assert b"0" in response.data

    assert b"Following" in response.data
    assert b"0" in response.data

    assert b"Public Repositories" in response.data
    assert b"0" in response.data

    # Avatar
    assert b"GitHub avatar URL" in response.data


@patch("src.routes.analyze.analyze_repository")
def test_owner_panel_handles_missing_owner(mock_analyze) -> None:
    """
    Verify owner panel renders safely when owner data is unavailable.

    Args:
        mock_analyze:
            Mock object used to verify the external call returns placeholder repository owner information.
    """

    analysis = mock_analysis_result()

    analysis["owner"]["name"] = ""
    analysis["owner"]["login"] = ""

    mock_analyze.return_value = analysis

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/analyze",
            data={
                "repository": "owner/repository"
            }
        )

    assert response.status_code == 200

    assert b"N/A" in response.data
