"""Add headers to external .md, .rst and .ipynb files."""

import json
from pathlib import Path


def format_header(cfg: dict, base_url: str, version: str) -> str:
    """Generate the admonition header based on the user's config."""
    # Check if language is set to Dutch in the configuration
    language = cfg.get("language", "en")

    if language == "nl":
        # Dutch attribution text
        admonition = (
            f"```{{{cfg['attribution_color']}}} Bronvermelding\n"
            ":class: attribution\n"
            f"Deze pagina is afkomstig van {base_url},"
            f" versie: {version}\n"
            "```\n"
        )
    else:
        # Default English attribution text
        admonition = (
            "```{" + cfg["attribution_color"] + "} Attribution\n"
            ":class: attribution\n"
            f"This page originates from {base_url},"
            f" version: {version}\n"
            "```\n"
        )

    if cfg["attribution_location"] == "top":
        return admonition

    return f"````{{margin}}\n{admonition}````\n"


def add_origin_notes(
    repo: Path, cfg: dict[str, str], base_url: str, version: str
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
        add_md_admonition(md_file, header)

    nb_files = repo.glob("**/*.ipynb")
    for nb_file in nb_files:
        add_nb_admonition(nb_file, header)

    rst_files = repo.glob("**/*.rst")
    for rst_file in rst_files:
        add_rst_admonition(rst_file, header)


def prepend(file: Path, text: str):
    """Prepend string `text` to plaintext file `file`."""
    original_content = file.read_text(encoding="utf-8")
    lines = original_content.splitlines()
    # Check if original_content contains a YAML top-matter metadata
    if len(lines) > 0 and lines[0] == "---":
        # Find the position of the closing `---`
        for i in range(1, len(lines)):
            if lines[i] == "---":
                # Insert after this line
                insert_pos = i + 1
                break
        else:
            insert_pos = 0  # No closing `---` found, treat as no YAML front matter

        # Reconstruct the content with the new text inserted after the YAML front matter
        yaml_content = "\n".join(lines[:insert_pos]) + "\n"
        rest_content = "\n".join(lines[insert_pos:])

        new_content = yaml_content + text + rest_content
    else:
        new_content = text + original_content
    file.write_text(new_content, encoding="utf-8")


def add_md_admonition(file: Path, header: str):
    """Add an admonition containing `text` to the top of markdown file `file`."""
    start_of_header_comment = "<!-- Start of inserted Teachbooks header -->"
    end_of_header_comment = "<!-- End of inserted Teachbooks header -->"
    header = f"{start_of_header_comment}\n\n{header}\n\n{end_of_header_comment}\n\n"
    prepend(file, header)


def add_rst_admonition(file: Path, header: str):
    """Add an admonition top of reST file.

    To do this we make use of the `include` directive and write the admonition
    as a separate markdown file which will be parsed by myst.
    """
    start_of_header_comment = ".. Start of inserted Teachbooks header"
    end_of_header_comment = ".. End of inserted Teachbooks header"
    header = f"{start_of_header_comment}\n\n{header}\n\n{end_of_header_comment}\n\n"
    admon_file = file.parent / f"_ad-{file.stem}.md"
    admon_file.write_text(header, encoding="utf-8")

    admonition = (
        f".. include:: {admon_file.name}\n    :parser: myst_parser.docutils_\n\n"
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
