from pathlib import Path

import pytest

from teachbooks.external_content.bib import merge_bibs, read_bibfile, write_bibfile
from tests.test_external_content import BOOK_ROOT
from tests.test_external_content import CLONED_REPOS


TEST_BIBFILE = (
    Path(__file__).parent / "testbook" / "book" / "_git" / 
    "gitlab.tudelft.nl_interactivetextbooks-citg_risk-and-reliability" / "main" /
    "book" / "_bibliography" / "references.bib"
)


@pytest.fixture
def merged_bibs():
    return merge_bibs(BOOK_ROOT / "references.bib", CLONED_REPOS)


def test_bib_merge(merged_bibs):
    """Ensure test data reference files are merged correctly."""
    assert len(merged_bibs) == 7 # total unique citekeys

    expected_entries = [
        "baecher2003", # duplicate
        "adk2022", # from risk-and-reliability
        "usace14", # from HOS-workbook
        "jason_moore",  # from excited workshop and main book
    ]
    citekeys = [bib.citekey for bib in merged_bibs]
    for entry in expected_entries:
        assert entry in citekeys


def test_bib_merge_duplicate(capsys, merged_bibs):
    """Warning should be raised when a duplicate entry is encountered."""
    err = capsys.readouterr()
    assert "duplicate citekey 'baecher2003'" in err.err


def test_read_write_bibfile(tmp_path):
    """Make sure that after writing the original bib file has the same content."""
    bibout = tmp_path / "references.bib"

    bibs = read_bibfile(TEST_BIBFILE)

    write_bibfile(bibout, bibs)

    assert bibs == read_bibfile(bibout)
