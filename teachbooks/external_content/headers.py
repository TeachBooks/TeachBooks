"""Add headers to external .md, .rst and .ipynb files."""

import json
from pathlib import Path


def add_origin_notes(repo: Path, base_url: str, version: str) -> None:
    """Add a note denoting the origin of a certain file.

    Args:
        repo: Path to the repository git cloned by the enternal-content routine.
        base_url: Base URL of the file's repository.
        version: Name of the version (tag, branch or commit hash).
    """
    header = (
        f"This page originates from a TeachBook hosted at {base_url},"
        f" version: {version}"
    )

    add_header_admonitions(repo, header)


def add_header_admonitions(repo: Path, text: str):
    """Add header to a file.

    Args:
        repo: .
        text: .
    """
    md_files = repo.glob("**/*.md")
    for md_file in md_files:
        add_md_admonition(md_file, text)
    
    rst_files = repo.glob("**/*.rst")
    for rst_file in rst_files:
        add_rst_admonition(rst_file, text)
    
    nb_files = repo.glob("**/*.ipynb")
    for nb_file in nb_files:
        add_nb_admonition(nb_file, text)


def prepend(file: Path, text: str):
    """Prepend string `text` to plaintext file `file`."""
    with file.open(mode="r") as f:
        original_content = f.read()

    with file.open(mode="w") as f:
        f.write(text + original_content)


def add_md_admonition(file: Path, text: str):
    """Add an admonition containing `text` to the top of markdown `file."""
    admonition = (
        ":::{attention}\n"
        f"{text}\n"
        ":::\n"
    )
    prepend(file, admonition)


def add_rst_admonition(file: Path, text: str):
    """Add an admonition containing `text` to the top of reST `file."""
    admonition = (
        ".. attention::\n"
        f"    {text}\n"
        "\n"
    )
    prepend(file, admonition)


def add_nb_admonition(file: Path, text: str):
    """Add an admonition containing `text` to the top of notebook `file."""
    with file.open("r") as f:
        notebook = json.load(f)
    
    admonition_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            ":::{attention}\n",
            f"{text}\n",
            ":::\n",
        ]
    }

    notebook["cells"] = [admonition_cell] + notebook["cells"]

    with file.open("w") as f:
        json.dump(notebook, f)
