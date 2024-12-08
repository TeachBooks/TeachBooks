import click
from pathlib import Path

@click.group()
@click.version_option()
def main():
    """TeachBooks command line tools"""
    pass

@main.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument("path-source", type=click.Path(exists=True, file_okay=True))
@click.option("--release", is_flag=True, help="Build book with release strategy")
@click.option("--publish", is_flag=True, help="--public is deprecated. Use --release instead.")
@click.option("--process-only", is_flag=True, help="Only pre-process content")
@click.pass_context
def build(ctx, path_source, publish, release, process_only):
    """Pre-process book contents and run Jupyter Book build command"""
    from teachbooks.release import make_release
    from jupyter_book.cli.main import build as jupyter_book_build

    if publish:
        click.secho("Warning: --publish is deprecated, use --release instead",
                    fg="yellow",
                    err=True)

    strategy = "release" if release or publish else "draft"
    echo_info(f"running build with strategy '{strategy}'")

    path_src_folder = Path(path_source).absolute()
    if release or publish:
        path_conf, path_toc = make_release(path_src_folder)
    else:
        path_conf = path_src_folder / "_config.yml"
        path_toc = path_src_folder / "_toc.yml"

    if not process_only:
        all_args = [str(path_src_folder)]
        if path_conf and path_conf.exists():
            all_args.extend(["--config", str(path_conf)])
        if path_toc and path_toc.exists():
            all_args.extend(["--toc", str(path_toc)])
        if ctx.args:
            all_args.extend(ctx.args)

        jupyter_book_build.main(args=all_args, standalone_mode=False)

        # Calculate and report build size
        build_dir = path_src_folder / "_build"
        total_size = sum(f.stat().st_size for f in build_dir.rglob('*') if f.is_file())
        size_mb = total_size / (1024 * 1024)
        echo_info(f"Build complete. Total size: {size_mb:.2f}MB")


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
# @click.argument("path-source", type=click.Path(exists=True, file_okay=True))
# @click.option("--test", is_flag=True, help="Build book with release strategy")
@click.option('-v', '--verbose', count=True)
@click.pass_context
def serve(ctx, verbose):
    """Start a web server to interact with the book locally.
    
    If serve dir path not provided, default is `./book/_build/html`.
    Checks to see if server is already running.
    """
    from teachbooks.serve import Server
    from teachbooks import SERVER_WORK_DIR, BOOK_SERVE_DIR

    if verbose > 0:
        echo_info(f"serve command invoked.")

    if ctx.invoked_subcommand is None:

        try:
            server = Server.load(Path(SERVER_WORK_DIR))
            if verbose > 0:
                echo_info(f" server already exists")
            
            stdout_summary(server)
        except:
            if verbose > 0:
                echo_info(f"no server found, creating a new one.")

            dir = Path(BOOK_SERVE_DIR)

            if not dir.exists():
                echo_info(click.style("default directory not found: ", fg="yellow") + f"{dir}")
                dir = Path(".")
                print('            '
                      +click.style("serving current directory: ", fg="yellow") + f"{dir}")
                print('            '
                      +click.style("specify a directory with: 'teachbooks serve path <path>'", fg="yellow"))
                
            serve_path(dir, verbose)

        # Hardcoded for now 
        # dir = Path("./book/_build/html")
        # echo_info(f"directory not provided; try {dir}")

        # if not dir.exists():
        #     dir = Path(".")
        #     echo_info(f"directory not found; using {dir}")

        # if verbose > 0:
        #     print(f"attempting to serve directory {dir}")

        

@serve.command()
@click.option('-v', '--verbose', count=True)
@click.argument("path-source",
                type=click.Path(exists=True, file_okay=True))
def path(path_source, verbose, no_build=False):
    """Specify relative path of directory to serve."""
    from teachbooks.serve import Server
    from teachbooks import BUILD_DIR, SERVER_WORK_DIR
    
    if verbose > 0:
        print(f"desired serve directory: {dir}")

    dir_with_build = Path(path_source).joinpath(BUILD_DIR)
    if dir_with_build.exists():
        dir = dir_with_build
        echo_info(f"_build/html available and appended to path.")
    else:
        dir = Path(path_source)

    # if not dir.exists():
    #     echo_info(click.style("*desired directory not found*: ", fg="yellow") + f"{dir}")
    #     dir = Path(".")
    #     print('            '
    #           +click.style("try current directory instead: ", fg="yellow") + f"{dir}")
    echo_info(f"attempting to serve this directory: {dir}")
    try:
        server = Server.load(Path(SERVER_WORK_DIR))
        if server.servedir == dir:
            print('            '
                  +f"  ---> already serving this directory.")
            stdout_summary(server)
        else:
            print('            '
                  +f"  ---> already serving a different directory.")
            print('            '
                  +f"  ---> updating server directory...")
            server.stop()
            serve_path(dir, verbose)
    except:
        if verbose > 0:
            echo_info(f"no server found, creating a new one.")
        serve_path(dir, verbose)

@serve.command()
def stop():
    """Stop the webserver."""
    from teachbooks.serve import Server
    from teachbooks import SERVER_WORK_DIR
    try:
        server = Server.load(Path(SERVER_WORK_DIR))
        server.stop()
        echo_info(f"server stopped.")
    except:
        echo_info(f"no server found.")


def serve_path(dir: str,
               verbose: int) -> None:
    """Start web server with specific path and verbosity."""
    from teachbooks.serve import Server
    from teachbooks import SERVER_WORK_DIR

    server = Server(servedir=Path(dir),
                    workdir=Path(SERVER_WORK_DIR),
                    stdout=verbose)
    server.start(options=["--all"])
    
    stdout_summary(server)
    

def echo_info(message: str) -> None:
    """Wrapper for writing to stdout."""
    prefix = click.style("TeachBooks: ", fg="cyan", bold=True)
    click.echo(prefix + message)

def stdout_summary(server) -> None:
    """Print summary of server status."""
    echo_info(click.style(f"server running on: {server.url}", fg="green"))
    print('            '
          +click.style(f"serving directory: {server.servedir}", fg="green"))
    print("            "
          +"To stop server, run: 'teachbooks serve stop'")