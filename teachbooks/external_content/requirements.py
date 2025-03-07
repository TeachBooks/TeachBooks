from pathlib import Path
import click


def check_requirements(main_requirements: Path, git_repos: list[Path]):
    if not main_requirements.exists():
        click.secho(
            "Warning: no requirements.txt file found for the main book.\n"
            "    TeachBooks will not be able to find which external-content"
            "dependencies are missing",
            fg="yellow",
            err=True,
        )
        return None

    requirements = read_requirements(main_requirements)

    repos = (repo for repo in git_repos if (repo / "requirements.txt").exists())
    for repo in repos:
        repo_requirements = read_requirements(repo / "requirements.txt")
        unmatched_requirements = repo_requirements - requirements
        if len(unmatched_requirements) > 0:
            unmatched_str = "".join(
                [f"       {req}\n" for req in unmatched_requirements]
            )
            click.secho(
                "Warning: requirements do not match between external content "
                "and your book\n"
                f"    Repository: {repo}\n"
                "    Missing or non-matching requirements:\n"
                f"{unmatched_str}"
                "Content from this book might not display or function correctly.",
                fg="yellow",
                err=True,
            )


def read_requirements(file: Path) -> set[str]:
    """Read requirements file and strip comments, index urls, and empty lines"""
    with file.open("r") as f:
        requirements = f.readlines()
    
    valid_requirements = set()
    for req in requirements:
        req = req.strip("\n\r")

        if len(req) == 0:
            pass
        elif req.startswith("#"):
            pass
        elif req.startswith("--"):
            pass
        else:
            valid_requirements.add(req.split(" #")[0])

    return valid_requirements
