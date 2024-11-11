# Keep top-level imports to a minimum to improve responsiveness
import click
from pathlib import Path


@click.group()
def main():
    """TeachBooks command line tools"""
    pass


@main.command()
@click.argument("path-source", type=click.Path(exists=True, file_okay=True))
@click.option(
    "--publish",
    is_flag=True,
    help="(Deprecated) Target publish version of the book. Use --release instead. "
         "Removes any sections surrounded by REMOVE-FROM-PUBLISH or REMOVE-FROM-RELEASE tags from _config.yml and _toc.yml"
)
@click.option(
    "--release",
    is_flag=True,
    help="Target release version of the book. Removes any sections surrounded "
         "by REMOVE-FROM-PUBLISH or REMOVE-FROM-RELEASE tags from _config.yml and _toc.yml"
)
@click.option(
    "--process-only",
    is_flag=True,
    help="Only pre-process content, do not build the book"
)
@click.pass_context
def build(ctx, path_source, publish, release, process_only):
    """Pre-process book contents and run the Jupyter Book build command"""

    from teachbooks.publish import make_publish
    from jupyter_book.cli.main import build as jupyter_book_build

    # Deprecation warning for --publish
    if publish:
        click.echo(click.style("The --publish option is deprecated, use --release instead.", fg="yellow"))

    # Prioritize --release if both are provided
    strategy = "release" if release or publish else "draft"
    echo_info(f"running build with strategy '{strategy}'")

    path_src_folder = Path(path_source).absolute()
    if release or publish:
        path_conf, path_toc = make_publish(path_src_folder)
    else:
        path_conf, path_toc = None, None

    # Use default arguments for jb build, as we normally do
    if not process_only:
        ctx.invoke(
            jupyter_book_build,
            path_source=path_src_folder,
            config=path_conf,
            toc=path_toc
        )
        ctx.invoke(
            jupyter_book_build,
            path_source=path_src_folder,
            config=path_conf,
            toc=path_toc,
            builder="linkcheck"
        )


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
        dir = Path("./book/_build/html/")
        workdir = Path("./book/.teachbooks/server")
        server = Server(servedir=dir, workdir=workdir)

        server.start()
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
