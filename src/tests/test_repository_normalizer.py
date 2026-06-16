"""
Automated tests for repository normalization.
"""

import pytest

from src.services.github.repository_normalizer import (
    RepositoryNormalizationError,
    RepositoryNormalizer,
)


def test_owner_repository_format_is_accepted() -> None:
    """Verify 'owner/repository' input format is unchanged."""

    result = RepositoryNormalizer.normalize("owner/repository")

    assert result == "owner/repository"


@pytest.mark.parametrize(
    "repository_input",
    [
        "https://github.com/owner/repository",
        "http://github.com/owner/repository",
        "github.com/owner/repository",
        "www.github.com/owner/repository"
    ]
)
def test_github_repo_url_is_normalized(repository_input: str) -> None:
    """Verify GitHub repository URL is converted to 'owner/repository'."""

    result = RepositoryNormalizer.normalize(repository_input)

    assert result == "owner/repository"


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
def test_github_url_without_repository_raises_error(repository_input: str) -> None:
    """Verify GitHub repository URLs without an 'owner/repository' included is rejected."""

    with pytest.raises(RepositoryNormalizationError):
        RepositoryNormalizer.normalize(repository_input)



def test_invalid_repository_format_raises_error() -> None:
    """Verify invalid repository input raises error."""

    with pytest.raises(RepositoryNormalizationError):
        RepositoryNormalizer.normalize(".")


@pytest.mark.parametrize(
    "repository_input",
    [
        "https://github.com/owner/repository.git",

        "http://github.com/owner/repository.git",

        "github.com/owner/repository.git",

        "www.github.com/owner/repository.git"
    ]
)
def test_git_suffix_is_removed(repository_input: str) -> None:
    """Verify '.git' suffix is removed."""

    result = RepositoryNormalizer.normalize(repository_input)

    assert result == "owner/repository"


@pytest.mark.parametrize(
    "repository_input",
    [
        " owner/repository ",
        "\towner/repository\t",
        "\nowner/repository\n",
    ]
)
def test_whitespace_is_removed(repository_input) -> None:
    """Verify leading and trailing whitespaces are ignored."""

    result = RepositoryNormalizer.normalize(repository_input)

    assert result == "owner/repository"


@pytest.mark.parametrize(
    "repository_input",
    [
        "owner/repository",
        "owner-name/repository-name",
        "owner.name/repository.name",
        "owner_name/repository_name",
    ]
)
def test_valid_owner_repository_formats_are_accepted(repository_input: str) -> None:
    """Verify valid 'owner/repository' formats are accepted unchanged."""

    result = RepositoryNormalizer.normalize(repository_input)

    assert result == repository_input
