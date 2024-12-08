import re
import os
from pathlib import Path


def make_publish(sourcedir: Path) -> tuple[Path, Path]:
    """Pre-process files in a Jupyter Book directory"""
    # Make hidden directory that will contain the cleaned-up files
    workdir = sourcedir.joinpath(".teachbooks", "release")

    if not os.path.exists(workdir):
        os.makedirs(workdir)

    for file in ["_config.yml", "_toc.yml"]:
        clean_yaml(
            sourcedir.joinpath(file),
            workdir.joinpath(file)
        )

    return workdir.joinpath("_config.yml"), workdir.joinpath("_toc.yml")


def clean_yaml(path_source: str | Path, path_output: str | Path) -> None:
    """Removes sections marked with # <START|END> REMOVE-FROM-PUBLISH or REMOVE-FROM-RELEASE from a yaml file

    Does not require a specific indentation and can be used an unlimited number of times
    in the ``*.yml`` file. Commonly applied to ``_toc.yml`` and ``_config.yml`` files of a book.

    Example:
    .. code:: python
        - file: subdirectory_1/intro_page
        sections:
        - file: subdirectory_1/sub_page_1
        # START REMOVE-FROM-PUBLISH
        - file: subdirectory_1/sub_page_2
        # END REMOVE-FROM-PUBLISH
        # START REMOVE-FROM-RELEASE
        - file: subdirectory_1/sub_page_3
        # END REMOVE-FROM-RELEASE
        - file: subdirectory_2/intro_page

    """

    with open(path_source, mode="r", encoding="utf8") as f:
        yaml_source = f.read()

    # Regex to remove both PUBLISH and RELEASE tags
    yaml_output = re.sub(
        r"# START REMOVE-FROM-(PUBLISH|RELEASE)(.|\n)*?# END REMOVE-FROM-(PUBLISH|RELEASE)",
        "",
        yaml_source
    )

    with open(path_output, mode="w", encoding="utf8") as f:
        f.write(yaml_output)
