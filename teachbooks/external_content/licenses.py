from pathlib import Path

import click


LICENSE_MAPPING = {
    "MIT License": "MIT",
    "GNU AFFERO GENERAL PUBLIC LICENSE": "AGPL",
    "GNU GENERAL PUBLIC LICENSE": "GPL",
    "GNU LESSER GENERAL PUBLIC LICENSE": "LGPL",
    "Mozilla Public License": "Mozilla",
    "Apache License": "Apache",
    "CREATIVE COMMONS PUBLIC LICENSE": "CCPL",
    "Creative Commons Attribution-NonCommercial": "CC-BY-NC",
    "Creative Commons Attribution 4.0": "CC-BY-4.0",
    "Attribution 4.0 International": "CC-BY-4.0",
    "CC0 1.0 Universal": "CC0",
    "BSD 3-Clause License": "BSD3",
    "European Union Public Licence": "EUPL",
}


def validate_licenses(cloned_repos: list[Path], git_path: Path, error: bool):
    """Validate if the cloned repositories all have permisive licenses."""
    for repo_path in cloned_repos:
        repo_license = find_license(repo_path)
        if repo_license is None:
            msg = f"Could not find a (valid) license in repository {repo_path}"
            if error:
                raise ValueError(msg)
            else:
                click.secho(f"WARNING: {msg}", fg="yellow")


def find_license(repo_toplevel: str | Path) -> str | None:
    """Try to detect which license is being used by a repo."""
    if (Path(repo_toplevel) / "LICENSE").exists():
        license_file = (Path(repo_toplevel) / "LICENSE")
    elif (Path(repo_toplevel) / "LICENSE.md").exists():
        license_file = (Path(repo_toplevel) / "LICENSE.md")
    else:
        msg = (
            f"No license file found in git repository at {repo_toplevel}.\n"
            "Licenses must be named 'LICENSE' or 'LICENSE.md'."
        )
        raise FileNotFoundError(msg)

    with license_file.open("r", encoding="utf-8") as f:
        license_content = "".join(f.readlines())

    stripped_license = license_content.lower().strip(" \n\r")

    detected_license = None
    for license_text in LICENSE_MAPPING:
        if license_text.lower().strip(" \n\r") in stripped_license:
            detected_license = LICENSE_MAPPING[license_text]
            break
    
    return detected_license
