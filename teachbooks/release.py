"""Teachbooks release workflow."""
import os
import re
from pathlib import Path


def make_release(sourcedir: Path) -> tuple[Path, Path]:
    """Pre-process files in a Jupyter Book directory."""
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

def copy_ext(sourcedir: Path) -> None:
    """Copy _ext/ to support APA in release [TEMPORARY]."""
    # Make hidden directory that will contain the cleaned-up files
    ext_dir = sourcedir.joinpath("_ext")
    workdir = sourcedir.joinpath(".teachbooks", "release")

    if not os.path.exists(workdir):
        os.makedirs(workdir)

    try:
        for root, dirs, files in os.walk(ext_dir):
            for _dir in dirs:
                os.makedirs(
                    workdir.joinpath(
                        "_ext", Path(root).relative_to(ext_dir).joinpath(_dir)
                        ), exist_ok=True
                )
            for file in files:
                src_file = Path(root).joinpath(file)
                dest_file = workdir.joinpath(
                    "_ext", Path(root).relative_to(ext_dir).joinpath(file)
                )
                os.makedirs(dest_file.parent, exist_ok=True)
                with open(src_file, 'rb') as fsrc, open(dest_file, 'wb') as fdst:
                    fdst.write(fsrc.read())
        print("Copied _ext/ directory successfully.")
    except:  # noqa: E722 (TODO: isolate specific exception, or re-raise error.)
        print("Error copying _ext/ directory.")

def clean_yaml(path_source: str | Path, path_output: str | Path) -> None:
    """Removes marked sections from a yaml file.
     
    A marked section can be:
        - ``# <START|END> REMOVE-FROM-PUBLISH``
        - or ``# <START|END> REMOVE-FROM-RELEASE``

    Does not require a specific indentation and can be used an
    unlimited number of times in the ``*.yml`` file. Commonly
    applied to ``_toc.yml`` and ``_config.yml`` files of a book.

    Example:
        To remove sub_page_2 and sub_page_3 from publishing::

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
    with open(path_source, encoding="utf8") as f:
        yaml_source = f.read()

    # Regex to remove both PUBLISH and RELEASE tags
    re_pub_release = (
        r"# START REMOVE-FROM-(PUBLISH|RELEASE)(.|\n)*?"
        r"# END REMOVE-FROM-(PUBLISH|RELEASE)"
    )
    yaml_output = re.sub(
        re_pub_release,
        "",
        yaml_source
    )

    with open(path_output, mode="w", encoding="utf8") as f:
        f.write(yaml_output)
