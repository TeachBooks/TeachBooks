"""Add headers to external .md, .rst and .ipynb files."""

import json
from pathlib import Path


def format_header(cfg: dict, base_url: str, version: str) -> str:
    """Generate the admonition header based on the user's config."""
    admonition = (
        "```{" + cfg['attribution_color'] + "} Attribution\n"
        ":class: attribution\n"
        f"This page originates from {base_url},"
        f" version: {version}\n"
        "```\n"
    )
    if cfg["attribution_location"] == "top":
        return admonition

    return (
        "````{margin}\n"
        f"{admonition}"
        "````\n"
    )


def add_origin_notes(
    repo: Path, cfg: dict[str,str], base_url: str, version: str
) -> None:
    """Add a note denoting the origin of a certain file.

    Args:
        repo: Path to the repository git cloned by the enternal-content routine.
        cfg: TeachBooks configuration.
        base_url: Base URL of the file's repository.
        version: Name of the version (tag, branch or commit hash).
    """
    header = format_header(cfg, base_url, version)
    add_header_admonitions(repo, header)


def add_header_admonitions(repo: Path, header: str):
    """Add header to a file.

    Args:
        repo: Path to the git repo cloned by the external content routine.
        header: Preformatted admonition header
    """
    md_files = repo.glob("**/*.md")
    for md_file in md_files:
        prepend(md_file, header)

    nb_files = repo.glob("**/*.ipynb")
    for nb_file in nb_files:
        add_nb_admonition(nb_file, header)

    rst_files = repo.glob("**/*.rst")
    for rst_file in rst_files:
        add_rst_admonition(rst_file, header)


def prepend(file: Path, text: str):
    """Prepend string `text` to plaintext file `file`."""
    original_content = file.read_text(encoding="utf-8")
    file.write_text(text + original_content, encoding="utf-8")


def add_rst_admonition(file: Path, header: str):
    """Add an admonition top of reST file.
    
    To do this we make use of the `include` directive and write the admonition
    as a separate markdown file which will be parsed by myst.
    """
    admon_file = file.parent / f"_ad-{file.stem}.md"
    admon_file.write_text(header, encoding="utf-8")

    admonition = (
        f".. include:: {admon_file.name}\n"
        "    :parser: myst_parser.docutils_\n"
        "\n"
    )
    prepend(file, admonition)


def add_nb_admonition(file: Path, header: str):
    """Add an admonition containing `text` to the top of notebook `file."""
    notebook = json.loads(file.read_text(encoding="utf-8"))

    # Split over newlines, but add newline char back in at end of lines.
    source = header.split("\n")
    source = [line + "\n" for line in source]

    admonition_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": source,
    }

    notebook["cells"] = [admonition_cell] + notebook["cells"]

    with file.open("w") as f:
        json.dump(notebook, f)
