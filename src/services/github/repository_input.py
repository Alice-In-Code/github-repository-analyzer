from src.services.github.repository_normalizer import RepositoryNormalizer

def parse_repository_input(raw_input: str) -> str:
    """
    Takes raw user input and returns a normalized 'owner/repository' string.

    Raises RepositoryNormalizationError if invalid.

    Args:
        raw_input: Raw user input for repository name.

    Returns:
        String of a normalized repository name in 'owner/repository' format.
    """

    return RepositoryNormalizer.normalize(raw_input)
