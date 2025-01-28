def parse_folder_name(repo_url: str) -> str:
    """Parses the repository URL to extract the folder name.

    Args:
        repo_url (str): The URL of the GitHub repository.

    Returns:
        str: The name of the folder where the repository will be cloned.
    """
    return repo_url.rstrip('/').split('/')[-1]