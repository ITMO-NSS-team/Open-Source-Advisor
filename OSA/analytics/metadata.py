import logging
import os
from dataclasses import dataclass

import requests
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

logger = logging.getLogger("rich")


@dataclass
class RepositoryMetadata:
    """
    Dataclass to store GitHub repository metadata.
    """
    name: str
    full_name: str
    owner: str
    owner_url: str | None
    description: str | None

    # Repository statistics
    stars_count: int
    forks_count: int
    watchers_count: int
    open_issues_count: int

    # Repository details
    default_branch: str
    created_at: str
    updated_at: str
    pushed_at: str
    size_kb: int

    # Repository URLs
    clone_url_http: str
    clone_url_ssh: str
    contributors_url: str | None
    languages_url: str
    issues_url: str | None

    # Programming languages and topics
    language: str | None
    languages: list[str]
    topics: list[str]

    # Additional repository settings
    has_wiki: bool
    has_issues: bool
    has_projects: bool
    is_private: bool
    homepage_url: str | None

    # License information
    license_name: str | None
    license_url: str | None


def _parse_repository_metadata(repo_data: dict) -> RepositoryMetadata:
    """
    Converts raw repository data from GitHub API into dataclass.
    """
    languages = repo_data.get("languages", {})
    license_info = repo_data.get("license", {}) or {}
    owner_info = repo_data.get("owner", {}) or {}

    return RepositoryMetadata(
        name=repo_data.get("name", ""),
        full_name=repo_data.get("full_name", ""),
        owner=owner_info.get("login", ""),
        owner_url=owner_info.get("html_url", ""),
        description=repo_data.get("description", ""),
        stars_count=repo_data.get("stargazers_count", 0),
        forks_count=repo_data.get("forks_count", 0),
        watchers_count=repo_data.get("watchers_count", 0),
        open_issues_count=repo_data.get("open_issues_count", 0),
        default_branch=repo_data.get("default_branch", ""),
        created_at=repo_data.get("created_at", ""),
        updated_at=repo_data.get("updated_at", ""),
        pushed_at=repo_data.get("pushed_at", ""),
        size_kb=repo_data.get("size", 0),
        clone_url_http=repo_data.get("clone_url", ""),
        clone_url_ssh=repo_data.get("ssh_url", ""),
        contributors_url=repo_data.get("contributors_url"),
        languages_url=repo_data.get("languages_url", ""),
        issues_url=repo_data.get("issues_url"),
        language=repo_data.get("language", ""),
        languages=list(languages.keys()) if languages else [],
        topics=repo_data.get("topics", []),
        has_wiki=repo_data.get("has_wiki", False),
        has_issues=repo_data.get("has_issues", False),
        has_projects=repo_data.get("has_projects", False),
        is_private=repo_data.get("private", False),
        homepage_url=repo_data.get("homepage", ""),
        license_name=license_info.get("name", ""),
        license_url=license_info.get("url", ""),
    )


def _get_base_repo_url(repo_url: str = None) -> str:
    """Extracts the base repository URL path from a given GitHub URL.

    Args:
        repo_url (str, optional): The GitHub repository URL. If not provided,
            the instance's `repo_url` attribute is used. Defaults to None.

    Returns:
        str: The base repository path (e.g., 'username/repo-name').

    Raises:
        ValueError: If the provided URL does not start with 'https://github.com/'.
    """
    if repo_url.startswith("https://github.com/"):
        base_repo_path = repo_url[len("https://github.com/"):].rstrip('/')
        return f"https://api.github.com/repos/{base_repo_path}"
    else:
        raise ValueError("Unsupported repository URL format.")


def _load_data_metadata(repo_url: str) -> RepositoryMetadata | None:
    """
    Retrieves GitHub repository metadata and returns a dataclass.
    """
    try:
        headers = {
            "Authorization": f"token {os.getenv('GIT_TOKEN')}",
            "Accept": "application/vnd.github.v3+json"
        }
        url = _get_base_repo_url(repo_url)

        response = requests.get(url=url, headers=headers)
        response.raise_for_status()

        metadata = response.json()
        logger.info(f"Successfully fetched metadata for repository: {repo_url}")
        return _parse_repository_metadata(metadata)
    except requests.RequestException as exc:
        logger.error(f"Error while fetching repository metadata: {exc}")
        raise
