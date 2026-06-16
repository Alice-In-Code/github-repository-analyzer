"""
Automated tests for application routes.
"""



from unittest.mock import patch

import pytest

from src.app import create_app


def test_homepage_loads() -> None:
    """
    Verify homepage loads successfully.
    """

    app = create_app()

    with app.test_client() as client:
        response = client.get("/")

    assert response.status_code == 200


@patch("src.routes.analyze.get_repository")
def test_repository_not_found_returns_404(mock_get) -> None:
    """Verify missing repositories return a 404 response."""

    mock_get.return_value = None

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
    """Verify empty repository input returns a 400 response."""

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/analyze",
            data={
                "repository": repository_input
            }
        )

    assert response.status_code == 400
    print(response.data.decode())
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
@patch("src.routes.analyze.get_repository")
def test_github_url_input_is_normalized(
        mock_get,
        repository_input: str
) -> None:
    """Verify GitHub repository URL inputs are normalized before API request."""

    mock_get.return_value = {"name": "repository"}

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/analyze",
            data={
                "repository": repository_input
            }
        )

    assert response.status_code == 200

    mock_get.assert_called_once_with(
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
    """Verify incomplete GitHub repository URLs return 400 Error."""

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/analyze",
            data={
                "repository": repository_input
            }
        )

    assert response.status_code == 400


@patch("src.routes.analyze.get_repository")
def test_owner_repository_input_returns_200(mock_get) -> None:
    """Verify 'owner/repository' input is accepted and returns 200."""

    mock_get.return_value = {
        "name": "repository"
    }

    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/analyze",
            data={
                "repository": "owner/repository"
            }
        )

    assert response.status_code == 200

    mock_get.assert_called_once_with(
        "owner/repository"
    )