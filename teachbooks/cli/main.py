import click
import os
import yaml
from pathlib import Path

@click.group()
def main():
    """TeachBooks command line tools"""
    pass

@main.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument("path-source", type=click.Path(exists=True, file_okay=True))
@click.option("--release", is_flag=True, help="Target release version of the book")
@click.option("--publish", is_flag=True, help="(Deprecated) Use --release instead")
@click.option("--process-only", is_flag=True, help="Only pre-process content")
@click.option("--check-thebe", is_flag=True, help="Check for Thebe files and their status")
@click.pass_context
def build(ctx, path_source, publish, release, process_only, check_thebe):
    """Pre-process book contents and run Jupyter Book build command"""
    from teachbooks.release import make_publish
    from jupyter_book.cli.main import build as jupyter_book_build

    if publish:
        click.secho("Warning: --publish is deprecated, use --release instead",
                   fg="yellow",
                   err=True)

    strategy = "release" if release or publish else "draft"
    echo_info(f"running build with strategy '{strategy}'")

    path_src_folder = Path(path_source).absolute()
    if release or publish:
        path_conf, path_toc = make_publish(path_src_folder)
    else:
        path_conf = path_src_folder / "_config.yml"
        path_toc = path_src_folder / "_toc.yml"

    if not process_only:
        # Start with base arguments
        all_args = [str(path_src_folder)]

        # Add config and toc if they exist
        if path_conf and path_conf.exists():
            all_args.extend(["--config", str(path_conf)])
        if path_toc and path_toc.exists():
            all_args.extend(["--toc", str(path_toc)])

        # Add all original args, preserving their order and values
        if ctx.args:
            all_args.extend(ctx.args)

        # Pass through all args to jupyter-book
        jupyter_book_build.main(args=all_args, standalone_mode=False)

        # Check for Thebe files if requested
        if check_thebe:
            build_dir = path_src_folder / "_build" / "html"
            excluded_files, included_files = check_thebe_files(build_dir, path_conf)
            report_thebe_status(excluded_files, included_files)


@main.command()
@click.argument("path-source", type=click.Path(exists=True, file_okay=True))
def clean(path_source):
    """Stop teachbooks server and run Jupyter Book clean command."""
    from jupyter_book.cli.main import clean as jupyter_book_clean
    from teachbooks.serve import Server, ServerError

    workdir = Path(path_source) / ".teachbooks" / "server"

    # Check if a server is running and stop it if so
    try:
        server = Server.load(workdir)
        if server.is_running:
            echo_info("Stopping running server before cleaning...")
            server.stop()
            echo_info("Server stopped.")
    except ServerError:
        echo_info("No running server found.")

    # Now proceed with cleaning
    echo_info(f"Cleaning build artifacts in {path_source}...")
    jupyter_book_clean.main([str(path_source)])
    echo_info("Clean complete.")


@main.group(invoke_without_command=True)
@click.pass_context
def serve(ctx):
    """Start a web server to interact with the book locally"""
    from teachbooks.serve import Server

    if ctx.invoked_subcommand is None:
        # Hardcoded for now
        dir = Path("./book")
        workdir = Path("./book/.teachbooks/server")
        server = Server(servedir=dir, workdir=workdir)

        server.start(options=["--all"])
        echo_info(f"server running on {server.url}")


@serve.command()
def stop():
    """Stop the webserver"""
    from teachbooks.serve import Server
    server = Server.load(Path("./book/.teachbooks/server"))
    server.stop()
    echo_info(f"server stopped")


def echo_info(message: str) -> None:
    """Wrapper for writing to stdout"""
    prefix = click.style("TeachBooks: ", fg="cyan", bold=True)
    click.echo(prefix + message)


def validate_thebe_config(config: dict) -> tuple[bool, list[str]]:
    """
    Validate Thebe configuration and return any issues found.

    Args:
        config: The loaded configuration dictionary

    Returns:
        tuple[bool, list[str]]: (is_valid, list of warning messages)
    """
    warnings = []
    is_valid = True

    thebe_config = config.get('thebe_config', {})

    # Check exclude_patterns
    exclude_patterns = thebe_config.get('exclude_patterns', [])
    if exclude_patterns == ["**/**"]:
        warnings.append("Warning: exclude_patterns is set to ['**/**'] which excludes all files. "
                        "Consider setting it to [] for no exclusions or specific patterns.")
        is_valid = False

    return is_valid, warnings


def check_thebe_files(build_dir: Path, config_path: Path) -> tuple[set[Path], set[Path]]:
    """
    Check for Thebe-related files in the build directory and validate against config.

    Args:
        build_dir: Path to the built book directory
        config_path: Path to the _config.yml file

    Returns:
        tuple[Set[Path], Set[Path]]: (excluded_files, included_files)
    """
    # Load configuration
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Validate config
    is_valid, warnings = validate_thebe_config(config)
    for warning in warnings:
        echo_info(warning)

    thebe_config = config.get('thebe_config', {})
    use_thebe = thebe_config.get('use_thebe_lite', False)
    exclude_patterns = thebe_config.get('exclude_patterns', [])

    if not use_thebe:
        return set(), set()

    # Known Thebe file patterns
    thebe_patterns = {
        "thebe.js",
        "thebe-lite.js",
        "thebe-core.js",
        "thebe-lite.css",
        "thebe-skeleton.css"
    }

    excluded_files = set()
    included_files = set()

    # Recursively search for Thebe files
    for root, _, files in os.walk(build_dir):
        root_path = Path(root)

        for file in files:
            if not any(thebe_pattern in file for thebe_pattern in thebe_patterns):
                continue

            file_path = root_path / file
            rel_path = file_path.relative_to(build_dir)
            str_path = str(rel_path)

            # Check if path matches any exclude pattern
            is_excluded = any(
                fnmatch(str_path, pattern)
                for pattern in exclude_patterns
            )

            if is_excluded:
                excluded_files.add(rel_path)
            else:
                included_files.add(rel_path)

    return excluded_files, included_files


def report_thebe_status(excluded_files: set[Path], included_files: set[Path]) -> None:
    """
    Report the status of Thebe files found during the build process.

    Args:
        excluded_files: Set of files matching exclude patterns
        included_files: Set of files not matching exclude patterns
    """
    if not (excluded_files or included_files):
        echo_info("No Thebe files found in the build.")
        return

    if included_files:
        echo_info("Included Thebe files:")
        for file in sorted(included_files):
            click.echo(f"  + {file}")

    if excluded_files:
        echo_info("Excluded Thebe files (matching exclude_patterns):")
        for file in sorted(excluded_files):
            click.echo(f"  - {file}")