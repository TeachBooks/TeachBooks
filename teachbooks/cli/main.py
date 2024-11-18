import click
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
@click.pass_context
def build(ctx, path_source, publish, release, process_only):
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