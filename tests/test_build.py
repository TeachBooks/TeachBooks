# Many book-related tests follow that set up in
# github.com/jupyter-book/jupyter-book/
from pathlib import Path
import pytest
from click.testing import CliRunner
from teachbooks.cli import main as commands

WORK_DIR = Path("./.teachbooks")
PATH_BOOKS = Path(__file__).parent.joinpath("books")

@pytest.fixture()
def cli():
    """Provides a click.testing CliRunner object for invoking CLI commands."""
    runner = CliRunner()
    yield runner
    del runner

def test_build(cli: CliRunner):
    book = PATH_BOOKS.joinpath("01")
    build_result = cli.invoke(commands.build,
                              book.as_posix())
    assert build_result.exit_code == 0, build_result.output
    html = book.joinpath("_build", "html")
    assert html.joinpath("index.html").exists()
    _ = cli.invoke(commands.clean,
                   book.as_posix())
    assert not html.joinpath("index.html").exists()

def test_build_release(cli: CliRunner):
    book = PATH_BOOKS.joinpath("01")
    build_result = cli.invoke(commands.build,
                              ['--release',
                              book.as_posix()])
    assert build_result.exit_code == 0, build_result.output
    html = book.joinpath("_build", "html")
    assert html.joinpath("index.html").exists()
    _ = cli.invoke(commands.clean,
                   book.as_posix())
    assert not html.joinpath("index.html").exists()

def test_build_publish(cli: CliRunner):
    book = PATH_BOOKS.joinpath("01")
    build_result = cli.invoke(commands.build,
                              ['--publish',
                              book.as_posix()])
    assert build_result.exit_code == 0, build_result.output
    html = book.joinpath("_build", "html")
    assert html.joinpath("index.html").exists()
    _ = cli.invoke(commands.clean,
                   book.as_posix())
    assert not html.joinpath("index.html").exists()