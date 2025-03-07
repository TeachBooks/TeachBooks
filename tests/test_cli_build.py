# Many book-related tests follow that set up in
# github.com/jupyter-book/jupyter-book/
from pathlib import Path
import pytest
from click.testing import CliRunner
from teachbooks.cli import main as commands


WORK_DIR = Path("./.teachbooks")
PATH_BOOKS = Path(__file__).parent / "books"


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
                              ["--release",
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
                              ["--publish",
                              book.as_posix()])
    assert build_result.exit_code == 0, build_result.output
    html = book.joinpath("_build", "html")
    assert html.joinpath("index.html").exists()
    _ = cli.invoke(commands.clean,
                   book.as_posix())
    assert not html.joinpath("index.html").exists()


def test_build_release_apa(cli: CliRunner):
    """Confirm _ext is copied into .teachbooks dir.
    
    Note that this does not test proper build, which
    must be done manually in a GitHub repo using the
    deploy-book-workflow with BRANCHES_TO_PREPROCESS.
    """
    book = PATH_BOOKS / "02"
    build_result = cli.invoke(commands.build, ["--release", book.as_posix()])
    assert build_result.exit_code == 0, build_result.output

    html = book / "_build" / "html"
    assert (html / "index.html").exists()
    
    ext_dir = book / ".teachbooks" / "release" / "_ext"
    assert (ext_dir / "apastyle.py").exists()
    assert (ext_dir / "bracket_citation_style.py").exists()
    assert (ext_dir / "pybtexapastyle").exists()
    assert (ext_dir / "pybtexapastyle" / "setup.py").exists()

    _ = cli.invoke(commands.clean, book.as_posix())
    assert not (html / "index.html").exists()

    # build 2x to make sure there aren't write conflicts within _ext
    build_result = cli.invoke(commands.build, ["--release", book.as_posix()])
    assert build_result.exit_code == 0, build_result.output
    assert (html / "index.html").exists()

    assert (ext_dir / "apastyle.py").exists()
    assert (ext_dir / "bracket_citation_style.py").exists()
    assert (ext_dir / "pybtexapastyle").exists()
    assert (ext_dir / "pybtexapastyle" / "setup.py").exists()


def test_build_external_content(cli: CliRunner):
    book = PATH_BOOKS.joinpath("03", "book")
    build_result = cli.invoke(commands.build,
                              book.as_posix())
    assert build_result.exit_code == 0, build_result.output
    assert (book / "_git").exists()
    html = book.joinpath("_build", "html")
    assert html.joinpath("index.html").exists()

    # TODO: cleaning this book can make second test book 03 to fail on some systems;
    _ = cli.invoke(commands.clean, ["--external", book.as_posix()])
    assert not html.joinpath("index.html").exists()
    assert not book.joinpath("_git").exists()


def test_build_release_external_content(cli: CliRunner):
    book = PATH_BOOKS.joinpath("03", "book")
    build_result = cli.invoke(commands.build,
                              ["--release",
                              book.as_posix()])
    assert build_result.exit_code == 0, build_result.output
    assert book.joinpath("_git").exists()
    html = book.joinpath("_build", "html")
    assert html.joinpath("index.html").exists()

    _ = cli.invoke(commands.clean, ["--external", book.as_posix()])
    assert not html.joinpath("index.html").exists()
    assert not book.joinpath("_git").exists()
