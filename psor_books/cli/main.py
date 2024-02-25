import click

from pathlib import Path
from jupyter_book.cli.main import build as jupyter_book_build

from psor_books.publish import make_publish

@click.group()
def main():
    """PSOR-Books command line tools"""
    pass

@main.command()
@click.argument("path-source", type=click.Path(exists=True, file_okay=True))
@click.option(
    "--publish",
    is_flag=True,
    help="Target publish version of the book. Removes any sections surrounded "
    "by REMOVE-FROM-PUBLISH tags from _config.yml and _toc.yml"
)
@click.option(
    "--process-only",
    is_flag=True,
    help="Only pre-process content, do not build the book"
)
@click.pass_context
def build(ctx, path_source, publish, process_only):
    """Pre-process book contents and run the Jupyter Book build command"""
    path_src_folder = Path(path_source).absolute()
    if publish:
        click.echo("Building publish book...")
        path_conf, path_toc = make_publish(path_src_folder)
    else:
        click.echo("Building draft book...")
        path_conf = None
        path_toc = None

    # Use default arguments for jb build, as we normally do
    if not process_only:
        ctx.invoke(
            jupyter_book_build,
            path_source=path_src_folder,
            config=path_conf,
            toc=path_toc
        )
