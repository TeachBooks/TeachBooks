from pathlib import Path
import pytest
from click.testing import CliRunner
from teachbooks.cli import main as commands

SERVE_DIR = Path(".")
WORK_DIR = Path("./.teachbooks")
PATH_BOOKS = Path(__file__).parent.joinpath("books")

@pytest.fixture()
def cli():
    """Provides a click.testing CliRunner object for invoking CLI commands."""
    runner = CliRunner()
    yield runner
    del runner

def test_serve_stop(cli: CliRunner):
    book = PATH_BOOKS.joinpath("01")
    build_result = cli.invoke(commands.build,
                              book.as_posix())
    assert build_result.exit_code == 0, build_result.output

    serve_result = cli.invoke(commands.serve)
    assert serve_result.exit_code == 0, serve_result.output

    stop_result = cli.invoke(commands.stop)
    assert stop_result.exit_code == 0, stop_result.output

    # Don't clean book, as we can continue using build directory

def test_path(cli: CliRunner):
    """Test basic usage: serve path <path>"""
    book = PATH_BOOKS.joinpath("01")

    path_result = cli.invoke(commands.serve,
                             ['path', book.as_posix()])
    assert path_result.exit_code == 0, path_result.output

    serve_result = cli.invoke(commands.serve)
    assert serve_result.exit_code == 0, serve_result.output

    stop_result = cli.invoke(commands.stop)
    assert stop_result.exit_code == 0, stop_result.output
    
# To add:
# - check output to see that directory moved
# - confirm that server is running at expected path
    
def test_path_unavailable(cli: CliRunner):
    """Test basic usage: serve path <path>"""
    path_unavailable = PATH_BOOKS
    path_available = PATH_BOOKS.joinpath("01")

    path_result = cli.invoke(commands.serve,
                             ['path', path_unavailable.as_posix()])
    assert path_result.exit_code == 0, path_result.output

    serve_result = cli.invoke(commands.serve,
                              ['path', path_available.as_posix()])
    assert serve_result.exit_code == 0, serve_result.output

    stop_result = cli.invoke(commands.stop)
    assert stop_result.exit_code == 0, stop_result.output