from teachbooks.external_content.config import check_plugins, find_config, find_plugins
from tests.test_external_content import BOOK_ROOT, CLONED_REPOS


def test_find_config_book():
    assert find_config(BOOK_ROOT.parent) == BOOK_ROOT / "_config.yml"


def test_find_config_repo():
    cfg_path = find_config(
        BOOK_ROOT / "_git/github.com_EXCITED-CO2_workshop_tutorial/v1.0.0"
    )
    expected_path = (
        BOOK_ROOT / "_git/github.com_EXCITED-CO2_workshop_tutorial/v1.0.0/book/_config.yml"
    )
    assert cfg_path == expected_path


def test_find_config_missing(tmp_path, capsys):
    result = find_config(tmp_path)
    assert result is None
    err = capsys.readouterr()
    assert "no config detected" in err.err


def test_find_multiple_configs(tmp_path, capsys):
    for name in ("a", "b"):
        directory = tmp_path / name
        directory.mkdir()
        (directory / "_config.yml").touch()
    result = find_config(tmp_path)
    assert result is None
    err = capsys.readouterr()
    assert "more than one config detected" in err.err


def test_find_plugins():
    expected = {'sphinx_image_inverter', 'download_link_replacer', 'sphinx.ext.extlinks', 'sphinx.ext.imgconverter', 'jupyterbook_patches'}

    assert find_plugins(BOOK_ROOT / "_config.yml")[0] == expected


def test_find_myst_expensions():
    expected = (
        {'sphinx.ext.imgconverter', 'jupyterbook_patches', 'download_link_replacer'},
        {"amsmath", "dollarmath", "linkify"}
    )
    cfg_path = (
        BOOK_ROOT / "_git/github.com_TeachBooks_HOS-workbook/main/book/_config.yml"
    )
    assert find_plugins(cfg_path) == expected


def test_check_plugins(capsys):
    result = check_plugins(BOOK_ROOT / "_config.yml", CLONED_REPOS)
    expected = (
        {"fake_test_plugin"},
        {"amsmath", "dollarmath", "linkify"}
    )
    assert result == expected

    err = capsys.readouterr()
    assert "sphinx plugins do not match" in err.err
    assert "MYST extensions do not match" in err.err


def test_check_plugins_no_conflict(capsys):
    no_conflict_repos = [repo for repo in CLONED_REPOS if "EXCITED" in str(repo)]
    result = check_plugins(BOOK_ROOT / "_config.yml", no_conflict_repos)
    expected = (set(), set())
    assert result == expected

    err = capsys.readouterr()
    assert err.err == ""
