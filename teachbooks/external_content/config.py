
from pathlib import Path
from typing import Any

import click

from teachbooks.external_content.utils import load_yaml_file


CLICK_WARNING_KWARGS: dict[str, Any] = {"fg": "yellow", "err": True}


def check_plugins(config_file: Path, git_repos: list[Path]) -> tuple[set[str], set[str]]:
    """Check external configs for missing plugins/myst extensions and return them.

    The user will be warned if any plugins or extensions are missing/not the same
    version pin.
    
    :param config_file: Path to the config yaml file.
    :param git_repos: List of cloned git repositories.
    :return: The missing plugins and myst extensions.
    """
    plugins, myst_extensions = find_plugins(config_file)

    missing_plugins: set[str] = set()
    missing_extensions: set[str] = set()

    for repo in git_repos:
        repo_config = find_config(repo)
        if repo_config is not None:
            repo_plugins, repo_myst_ext = find_plugins(repo_config)
            unmatched_plugins = repo_plugins - plugins
            unmatched_extensions = repo_myst_ext - myst_extensions

            missing_plugins = missing_plugins | unmatched_plugins
            missing_extensions = missing_extensions | unmatched_extensions

            if len(unmatched_plugins) > 0:
                unmatched_str = "".join(
                    [f"       {req}\n" for req in unmatched_plugins]
                )
                click.secho(
                    "Warning: sphinx plugins do not match between external content "
                    "and your book\n"
                    f"    Repository: {repo}\n"
                    "    Missing or non-matching plugins:\n"
                    f"{unmatched_str}"
                    "Content from this book might not display correctly.",
                    **CLICK_WARNING_KWARGS
                )

            if len(unmatched_extensions) > 0:
                unmatched_str = "".join(
                    [f"       {req}\n" for req in unmatched_extensions]
                )
                click.secho(
                    "Warning: MYST extensions do not match between external content "
                    "and your book\n"
                    f"    Repository: {repo}\n"
                    "    Missing or non-matching extensions:\n"
                    f"{unmatched_str}"
                    "Content from this book might not display correctly.",
                    **CLICK_WARNING_KWARGS
                )
    return missing_plugins, missing_extensions


def find_config(repo: Path) -> Path | None:
    std_config = repo / "book" / "_config.yml"
    if std_config.exists():
        return std_config

    # book name might be different. Only search one directory level deep:
    detected_configs = list(repo.glob("*/_config.yml"))
    if len(detected_configs) == 1:
        return detected_configs[0]
    if len(detected_configs) > 1:
        msg = (
            "Warning: more than one config detected in external content repo,\n"
            "    could not validate config plugins/extensions."
            f"    Please check {repo}"
        )
        click.secho(msg, **CLICK_WARNING_KWARGS)    
    elif len(detected_configs) == 0:
        msg = (
            "Warning: no config detected in external content repo,\n"
            "    could not validate config plugins/extensions."
            f"    Please check {repo}"
        )
        click.secho(msg, **CLICK_WARNING_KWARGS)    
    return None


def find_plugins(config_file: Path) -> tuple[set[str], set[str]]:
    sphinx_plugins = get_sphinx_plugins(config_file)
    myst_extensions = get_myst_extensions(config_file)
    return sphinx_plugins, myst_extensions


def get_sphinx_plugins(config_file: Path) -> set[str]:
    """Find the sphinx plugins in the config file.
    
    :param config_file: Path to the config yaml file.
    :return: Sphinx plugin names as a set
    """
    config = load_yaml_file(config_file)

    sphinx_plugins = set()
    if config.get("sphinx") is None:
        msg = (
            "Warning: Missing 'sphinx' entry in config,\n"
            f"    Please check {config_file}"
        )
        click.secho(msg, **CLICK_WARNING_KWARGS)
    elif not isinstance(config.get("sphinx"), dict):
        msg = (
            "Malformed 'sphinx' entry in config (expected sub-entries),\n"
            f"    Please check {config_file}"
        )
        click.secho(msg, **CLICK_WARNING_KWARGS)
    elif config.get("sphinx").get("extra_extensions") is None:
        msg = (
            "Malformed 'sphinx' entry in config (expected 'extra_extensions' entry),\n"
            f"    Please check {config_file}"
        )
        click.secho(msg, **CLICK_WARNING_KWARGS)
    else:
        sphinx_plugins = set(config.get("sphinx").get("extra_extensions"))
    return sphinx_plugins


def get_myst_extensions(config_file: Path) -> set[str]:
    """Find the myst extensions in the config file.
    
    :param config_file: Path to the config yaml file.
    :return: myst extension names as a set
    """
    config = load_yaml_file(config_file)

    myst_extensions = set()
    if config.get("parse") is None:
        pass # "parse" entry is not required.
    elif not isinstance(config.get("parse"), dict):
        msg = (
            "Malformed 'parse' entry in config (expected sub-entries),\n"
            f"    Please check {config_file}"
        )
        click.secho(msg, **CLICK_WARNING_KWARGS)
    elif config.get("parse").get("myst_enable_extensions") is None:
        msg = (
            "Malformed 'parse' entry in config (expected 'myst_enable_extensions' entry),\n"
            f"    Please check {config_file}"
        )
        click.secho(msg, **CLICK_WARNING_KWARGS)
    else:
        myst_extensions = set(config.get("parse").get("myst_enable_extensions"))
    return myst_extensions
