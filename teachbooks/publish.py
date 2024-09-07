import re
import os

from pathlib import Path


def make_publish(sourcedir: Path) -> tuple[Path, Path]:
    """Pre-process files in a Jupyter Book directory"""

    # Make hidden directory that will contain the cleaned-up files
    workdir = sourcedir.joinpath(".teachbooks", "publish")

    if not os.path.exists(workdir):
        os.makedirs(workdir)

    for file in ["_config.yml", "_toc.yml"]:
        clean_yaml(
            sourcedir.joinpath(file),
            workdir.joinpath(file)
        )

    return workdir.joinpath("_config.yml"), workdir.joinpath("_toc.yml")


def clean_yaml(path_source: str | Path, path_output: str | Path) -> None:
    """Removes sections marked with # REMOVE-FROM-PUBLISH from a yaml file"""

    with open(path_source, mode="r", encoding="utf8") as f:
        yaml_source = f.read()

    yaml_output = re.sub(
        r"# START REMOVE-FROM-PUBLISH(.|\n)*?# END REMOVE-FROM-PUBLISH", 
        "", 
        yaml_source
    )

    with open(path_output, mode="w", encoding="utf8") as f:
        f.write(yaml_output)
