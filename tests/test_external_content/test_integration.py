import shutil
import traceback
from pathlib import Path

import pytest
from click.testing import CliRunner

from teachbooks.cli import main as commands

WORK_DIR = Path(__file__).parent / ".teachbooks"
PATH_TESTDATA = Path(__file__).parent / "testbook"

ADMONITION_HTML = (
    '<div class="attribution admonition">'
    '<p class="admonition-title">Attribution</p>'
    "<p>This page originates from"
)


@pytest.fixture()
def cli():
    """Provides a click.testing CliRunner object for invoking CLI commands."""
    runner = CliRunner()
    yield runner
    del runner


def strip_whitespace(text: str) -> str:
    text = text.replace(" ", "")
    text = text.replace("\n", "")
    text = text.replace("\r", "")
    return text.replace("\t", "")


def test_build(cli: CliRunner, tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # Fix for windows on CI (otherwise relative dirs fail)
    # Copy test book to temp dir
    testdir: Path = shutil.copytree(PATH_TESTDATA, tmp_path / "test")
    bookdir = testdir / "book"

    # remove cloned_repos.txt file (to make clone routines run)
    repos = bookdir / "_git" / "cloned_repos.txt"
    repos.unlink()

    # Modify book config to be CI environment compatible
    config = bookdir / "_config.yml"
    testconfig = bookdir / "_config.test.yml"
    config.unlink()
    testconfig.rename(config)

    # Actually run tests
    build_result = cli.invoke(
        commands.build,
        bookdir.as_posix(),
        env={"NO_GIT_CLONE": ""},
    )

    if build_result.exit_code == 1:
        traceback.print_tb(build_result.exc_info[2])
    assert build_result.exit_code == 0, build_result.output

    indexfile = bookdir / "_build" / "html" / "index.html"
    _gitdir = bookdir / "_git"
    notebook_page = (
        bookdir
        / "_build"
        / "html"
        / "_git"
        / "github.com_EXCITED-CO2_workshop_tutorial"
        / "v1.0.0"
        / "book"
        / "ARCO-ERA5.html"
    )
    rst_page = (
        bookdir
        / "_build"
        / "html"
        / "_git"
        / "github.com_EXCITED-CO2_workshop_tutorial"
        / "v1.0.0"
        / "book"
        / "extra_file.html"
    )
    md_page = (
        bookdir
        / "_build"
        / "html"
        / "_git"
        / "github.com_TeachBooks_HOS-workbook"
        / "main"
        / "book"
        / "intro.html"
    )

    for path in (indexfile, _gitdir, notebook_page, rst_page, md_page):
        assert path.exists()

    for page in (notebook_page, rst_page, md_page):
        page_text = page.read_text()
        page_text = strip_whitespace(page_text)
        assert strip_whitespace(ADMONITION_HTML) in page_text

    _ = cli.invoke(
        commands.clean,
        ["--external", bookdir.as_posix()],
    )
    assert not indexfile.exists()
    assert not _gitdir.exists()
