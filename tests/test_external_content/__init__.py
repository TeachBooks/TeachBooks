from pathlib import Path

from teachbooks.external_content import GIT_PATH
from teachbooks.external_content.process_toc import read_cloned_repos


BOOK_ROOT = Path(__file__).parent / "testbook" / "book"
CLONED_REPOS = read_cloned_repos(BOOK_ROOT / GIT_PATH / "cloned_repos.txt")
