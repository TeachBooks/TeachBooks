"""Process git repo URLs."""
import re
from pathlib import Path


def get_repo_url(url: str) -> str:
    """Get repo url by searching for reg like ``https://*/*/*/``.

    Args:
        url: URL path to the external content
    
    Returns:
        repository URL
    """
    pattern = r"https://[^/]+/[^/]+/[^/]+(?=/)"
    match = re.search(pattern, url)
    if match is None:
        msg = (
        "Invalid external content URL. Could not parse repo URL from:\n"
        f" '{url}'"
        )
        raise ValueError(msg)
    return match[0]


def get_branch_tag_name(url: str) -> str:
    """Get branch_tag_name by searching for between blob and book in external_url.

    Args:
        url: URL path to the external content.
    
    Returns:
        branch or tag name.
    """
    pattern = r"blob/([^/]+)/"
    match = re.search(pattern, url)

    if match is None:
        msg = (
        "Invalid external content URL. Could not retrieve branch/tag name from:\n"
        f" '{url}'"
        )
        raise ValueError(msg)
    return match[1]


def create_repository_dir_name(url: str, root_dir: str | Path) -> str:
    """Generate the path where the repo will be cloned to.

    It will be of the form:

    {root_path}/{platform}_{organization}_{repository}/{revision}

    Args:
        url: URL path to the external content.
        root_dir: root directory where the repo will be cloned into.
    
    Returns:
        Path where the repo will be cloned to.
    """
    branch_tag_name = get_branch_tag_name(url)
    url = get_repo_url(url)
    if url.startswith("https://"):
        url = url.removeprefix("https://")
    dir_name = url.replace("/", "_")
    return f"{root_dir}/{dir_name}/{branch_tag_name}"
