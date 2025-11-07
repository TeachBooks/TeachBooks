"""Read and process table of contents files."""

import os.path
import stat
import subprocess
from pathlib import Path
from typing import Any

import click
import yaml

from teachbooks.external_content import GIT_PATH
from teachbooks.external_content.bib import merge_bibs, write_bibfile
from teachbooks.external_content.config import check_plugins, get_teachbooks_config
from teachbooks.external_content.git import (
    create_repository_dir_name,
    get_branch_tag_name,
    get_repo_url,
)
from teachbooks.external_content.headers import add_origin_notes
from teachbooks.external_content.licenses import validate_licenses
from teachbooks.external_content.requirements import check_requirements
from teachbooks.external_content.utils import load_yaml_file, modify_field

LOCAL_TOC_HEADER = (
    "ToC file with localized paths. Used for Teachbooks' external content feature."
)


def process_external_toc_entries(
    src: Path, dest: Path, book_root: Path, error_invalid_license: bool = True
) -> Path:
    """Parse external (git) ToC entries, checkout repos & write new ToC to file.

    Args:
        src: Path to the source table-of-contents yaml file.
        dest: Path to the destination table-of-contents yaml file.
        book_root: Path to the root of the book.
        error_invalid_license: If true, and no valid license is found in an
            external repository, an error will be raised. Else only a warning.

    Returns:
        Path to the new table-of-contents yaml file, or the original file
            if the toc was not modified.
    """
    src_toc = load_yaml_file(src)
    toc = src_toc.copy()

    toc = modify_field(
        toc,
        key="external",
        func=external_to_local,
        external_path=book_root / GIT_PATH,
        root=book_root,
    )

    cloned_repo_log = book_root / GIT_PATH / "cloned_repos.txt"
    if cloned_repo_log.exists():
        cloned_repos = read_cloned_repos(cloned_repo_log)
        validate_licenses(cloned_repos, book_root / GIT_PATH, error_invalid_license)
        check_requirements(book_root.parent / "requirements.txt", cloned_repos)
        check_plugins(book_root / "_config.yml", cloned_repos)

        merged_bibs = merge_bibs(book_root / "references.bib", cloned_repos)
        if len(merged_bibs) > 0:  # only write a file when there are bibtex entries
            write_bibfile(dest.parent / "references.bib", merged_bibs)
        # TODO: don't overwrite original references.bib file

        write_toc_yaml(toc, dest, header=LOCAL_TOC_HEADER)
        return dest

    if toc != src_toc:
        msg = (
            "Table of contents has external git content, "
            "but no git repositories were checked out.\n"
            "Please fix your table of content or remove any `external` entries"
        )
        raise ValueError(msg)
    return src


def read_cloned_repos(log: Path) -> list[Path]:
    """Read in cloned repo file to get paths to all cloned repos."""
    with log.open("r") as f:
        cloned_repos_str = [repo.strip("\n\r") for repo in f.readlines()]
    return [
        Path(repo) if Path(repo).is_absolute() else log.parent / repo
        for repo in cloned_repos_str
    ]


def get_content_path(url: str) -> str:
    """Get relative path of the external content from the URL path.

    Args:
        url: URL path to the external content

    Returns:
        repo path to the external content
    """
    branch_tag_name = get_branch_tag_name(url)
    *_, path = url.split(branch_tag_name)
    return path.strip("/")  # remove leading and trailing "/"


def write_toc_yaml(
    data: dict[str, str],
    path: str | Path,
    encoding: str = "utf8",
    header: str | None = None,
) -> None:
    """Write a ToC file.

    Args:
        data: site map
        path: Target `_toc.yml` file path
        encoding: `_toc.yml` file character encoding
        header: Commented out header to start toc file with.
    """
    with open(path, encoding=encoding, mode="w") as handle:
        if header is not None:
            handle.write(f"# {header}\n")
        yaml.safe_dump(data, handle)


def external_to_local(
    mapping: dict[str, Any], external_path: str | Path, root: str | Path
) -> dict[str, Any]:
    """Modify mapping with the "external" key.

    Retrieve external components locally, and fix ToC fields accordingly.

    Args:
        mapping: map to modify.
        external_path: path where to store external components.
        root: express paths to external components with respect to root.

    Returns:
        map with fields adjusted in order to refer to local resources.
    """
    cfg = get_teachbooks_config(root / "_config.yml")

    mapping_local = mapping.copy()
    external_url = mapping_local.pop("external")

    repo_url = get_repo_url(external_url)
    clone_url = f"{repo_url}.git"

    branch_tag_name = get_branch_tag_name(external_url)
    repository_dir = create_repository_dir_name(external_url, root_dir=external_path)

    cloned_repo_file = Path(external_path) / "cloned_repos.txt"
    if cloned_repo_file.exists():
        with open(cloned_repo_file) as f:
            cloned_repos = f.read()
    else:
        cloned_repos = []

    if repository_dir in cloned_repos:
        click.secho(f"{repository_dir} has already been cloned. Not re-downloading")
    else:
        # clone with branch_name. Check for environment var (for testing)
        if "NO_GIT_CLONE" not in os.environ:
            subprocess.run(
                [
                    "git",
                    "clone",
                    "--single-branch",
                    "-b",
                    branch_tag_name,
                    clone_url,
                    repository_dir,
                ]
            )
        with cloned_repo_file.open("a") as f:
            f.write(str(repository_dir) + "\n")

        add_origin_notes(Path(repository_dir), cfg, repo_url, version=branch_tag_name)

    content_file = get_content_path(external_url)
    rel_path = os.path.relpath(repository_dir, root)
    mapping_local["file"] = os.path.join(rel_path, content_file).replace("\\", "/")

    for k, v in list(mapping_local.items()):
        if isinstance(v, dict | list):
            mapping_local[k] = modify_field(
                v, "external", external_to_local, external_path=external_path, root=root
            )

    return mapping_local


def chmod_git_files(foo, file, err):
    """Remove git files on Windows.

    Solution from: https://stackoverflow.com/a/76356125
    """
    if (
        os.name == "nt"
        and Path(file).suffix in [".idx", ".pack", ".rev"]
        and err[0].__name__ == "PermissionError"
    ):
        os.chmod(file, stat.S_IWRITE)
        foo(file)
