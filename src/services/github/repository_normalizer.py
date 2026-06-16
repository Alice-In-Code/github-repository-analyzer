"""
Repository Normalization Service.

This module is responsible for converting user-provided GitHub repository inputs into a consistent format of
'owner/repository'.

This ensures that downstream services (e.g. GitHub API clients) recieve a valid format regardless of user input format.
"""

import re
from urllib.parse import urlparse


class RepositoryNormalizationError(ValueError):
    """Raised when repository input can't be normalized."""
    pass


class RepositoryNormalizer:
    """Normalizes GitHub repository inputs into a consistent 'owner/repository' format."""

    OWNER_REPO_REGEX = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")

    GITHUB_HOSTS = {"github.com", "www.github.com"}

    @classmethod
    def normalize(cls, repo_input: str) -> str:
        if not repo_input or not isinstance(repo_input, str):
            raise RepositoryNormalizationError(
                "Repository input must not be empty"
            )

        value = repo_input.strip()

        # Already in 'owner/repository' format.
        if cls.OWNER_REPO_REGEX.match(value):
            return value

        if value.startswith(
                (
                    "github.com/",
                    "www.github.com/",
                )
        ) or value in (
            "github.com",
            "www.github.com"
        ):
            value = f"https://{value}"

        if value.startswith(("http://", "https://")):
            return cls._normalize_from_url(value)

        raise RepositoryNormalizationError(
            """Invalid repository format. Expected 'owner/repository' or a GitHub repository URL 
            (e.g. https://github.com/owner/repository)."""
        )

    @classmethod
    def _normalize_from_url(cls, url: str) -> str:
        parsed = urlparse(url)

        if parsed.netloc not in cls.GITHUB_HOSTS:
            raise RepositoryNormalizationError(
                "Only GitHub URLs are supported"
            )

        parts = parsed.path.strip("/").split("/") # Extracts 'owner/repository' from GitHub URL.

        # Checking if repository input contains more than just an owner name.
        if len(parts) < 2:
            raise RepositoryNormalizationError(
                "Invalid GitHub repository URL, ensure to include both 'owner/repository'"
            )

        owner, repo = parts[0], parts[1]

        repo = repo.removesuffix(".git") # Removing trailing ".git" suffix.

        if not owner or not repo:
            raise RepositoryNormalizationError(
                "Invalid GitHub repository path"
            )

        return f"{owner}/{repo}"
