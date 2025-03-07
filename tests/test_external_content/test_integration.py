from pathlib import Path
import shutil
import pytest
from click.testing import CliRunner
from teachbooks.cli import main as commands


WORK_DIR = Path(__file__).parent / ".teachbooks"
PATH_TESTDATA = Path(__file__).parent / "testbook"


@pytest.fixture()
def cli():
    """Provides a click.testing CliRunner object for invoking CLI commands."""
    runner = CliRunner()
    yield runner
    del runner


def test_build(cli: CliRunner, tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # Fix for windows on CI (otherwise relative dirs fail)
    # Copy test book to temp dir
    testdir: Path = shutil.copytree(PATH_TESTDATA, tmp_path / "test")
    bookdir = testdir / "book"

    # Modify book config to be CI environment compatible
    config = bookdir / "_config.yml"
    testconfig = bookdir / "_config.test.yml"
    config.unlink()
    testconfig.rename(config)

    # Actually run tests
    build_result = cli.invoke(
        commands.build,
        bookdir.as_posix()
    )
    assert build_result.exit_code == 0, build_result.output

    indexfile = bookdir / "_build" / "html" / "index.html"
    _gitdir = bookdir / "_git"
    notebook_page = (
        bookdir / "_build" / "html" / "_git" /
        "github.com_EXCITED-CO2_workshop_tutorial" / "v1.0.0" / "book" /
        "ARCO-ERA5.html"
    )
    
    for path in (indexfile, _gitdir, notebook_page):
        assert path.exists()

    _ = cli.invoke(commands.clean,
                   ['--external',
                   bookdir.as_posix()],)
    assert not indexfile.exists()
    assert not _gitdir.exists()
