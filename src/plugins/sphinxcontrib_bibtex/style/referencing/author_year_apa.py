from dataclasses import dataclass, field

from sphinxcontrib.bibtex.style.referencing import BracketStyle
from sphinxcontrib.bibtex.style.referencing.author_year import AuthorYearReferenceStyle

def bracket_style() -> BracketStyle:
    return BracketStyle(left='(', right=')')

@dataclass
class AuthorYearRoundReferenceStyle(AuthorYearReferenceStyle):
    bracket_parenthetical: BracketStyle = field(default_factory=bracket_style)
    bracket_textual: BracketStyle = field(default_factory=bracket_style)
    bracket_author: BracketStyle = field(default_factory=bracket_style)
    bracket_label: BracketStyle = field(default_factory=bracket_style)
    bracket_year: BracketStyle = field(default_factory=bracket_style)
