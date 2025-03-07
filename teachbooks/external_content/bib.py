"""Functionality to read write and compare .bib files."""
from dataclasses import dataclass
import re
from pathlib import Path

import click

from teachbooks.external_content.config import CLICK_WARNING_KWARGS


BIB_ENTRY_RE = re.compile(r"@(\w+){([\w:-]+)")


@dataclass
class BibEntry:
    """Contains all information of a bib file entry."""
    entrytype: str
    citekey: str
    content: dict[str,str]


def read_bibfile(file: Path) -> list[BibEntry]:
    """Read bib file into list of BibEntry objects.

    :param file: Path to the .bib file.
    :return: List of .bib file entries.
    """
    with file.open("r") as f:
        lines = f.readlines()

    entries: list[str] = []
    for line in lines:
        if len(line.strip()) > 0:
            matches = BIB_ENTRY_RE.match(line)
            if matches:
                entries.append("")
            entries[-1] += line

    bib_entries: list[BibEntry] = []
    for entry in entries:
        e = entry.strip().splitlines()
        entrytype, citekey = BIB_ENTRY_RE.findall(e.pop(0))[0]

        content = {}
        for line in e:
            i_eq = line.find("=")  # index of = sign; splits key and value
            if i_eq != -1:
                key = line[:i_eq].strip()
                val = line[i_eq+1:]
                leading_br = val.find("{")
                trailing_br = len(val)-val[::-1].find("}")
                content[key] = val[leading_br+1:trailing_br-1]
        
        if len(content) > 0:
            bib_entries.append(
                BibEntry(entrytype, citekey, content)
            )
        else:
            msg = f"Malformed entry ({citekey}) found in .bib file: {file}"
            click.secho(msg)

    return bib_entries


def bib_union(bibs: list[BibEntry], additional_bibs: list[BibEntry]):
    """Join two lists of .bib file entries, checking for duplicate keys.

    If the citekey exists in both lists, the title is checked. If the title
    is the same, it is assumed that the reference already exists in the main list,
    and is skipped silently. If the titles do not match, a warning is given.

    :param bibs: Main list of bib entries.
    :param additional_bibs: List of additional bib entries you want to add to 
        the main list.
    :return: Joined list of .bib file entries.
    """
    bib_citekeys = set(bib.citekey for bib in bibs)
    extra_citekeys = set(bib.citekey for bib in additional_bibs)
    overlap = bib_citekeys.intersection(extra_citekeys)

    if len(overlap) == 0:  # no overlap: clean join
        return bibs + additional_bibs

    merged_bibs = bibs.copy()
    for entry in additional_bibs:
        if entry.citekey not in overlap:
            merged_bibs.append(entry)
        else:  # citekey already exists. check if title is the same
            bib_title = find(entry.citekey, bibs).content["title"]
            if bib_title == entry.content["title"]:
                pass
            else:
                msg = (
                    f"Warning: Found duplicate citekey '{entry.citekey}'in bibfile.\n"
                    "    However, the titles did not match.\n"
                    "    References in external content might be incorrect!"
                )
                click.secho(msg, **CLICK_WARNING_KWARGS)

    return merged_bibs


def find(citekey: str, bibs: list[BibEntry]) -> BibEntry:
    """Find bib entry by citekey"""
    key_index = [bib.citekey == citekey for bib in bibs].index(True)
    return bibs[key_index]


def write_bibfile(file: Path, bibs: list[BibEntry]) -> None:
    """Write a list of BibEntries to a new file."""
    with open(file, "w") as f:
        for bib in bibs:
            content_strs = [
                f"  {key} = {{{val}}}" for key, val in bib.content.items()
            ]
            entry = (
                f"@{bib.entrytype}{{{bib.citekey},\n" +\
                ",\n".join(content_strs) +\
                ",\n}\n\n"
            )
            f.write(entry)


def merge_bibs(bibfile: Path, repos: list[Path]) -> list[BibEntry]:
    """Merge the book's .bib file with all external bibs.
    
    Will return an empty list if no reference.bib files are present anywhere.
    """
    if bibfile.exists():
        book_bib = read_bibfile(bibfile)
    else:
        book_bib = []

    for repo in repos:
        repo_bibfile = find_bibfile(repo)
        if repo_bibfile is not None:
            extra_bibs = read_bibfile(repo_bibfile)
            book_bib = bib_union(book_bib, extra_bibs)
    
    return book_bib


def find_bibfile(repo: Path) -> Path | None:
    """Try to find the references.bib file in the usual locations."""
    expected_location = repo / "book" / "references.bib"
    if expected_location.exists():
        return expected_location

    # main dir might not be named "book"
    possible_bibs = list(repo.glob("*/references.bib"))
    if len(possible_bibs) == 0: # bib file might be in subdir
        possible_bibs = list(repo.glob("*/*/references.bib"))
    if len(possible_bibs) == 1:
        return possible_bibs[0]
    if len(possible_bibs) > 1:
        msg = (
            "Warning: more than one references.bib file detected in external\n"
            "     content repo, could not merge references into main file."
            f"    Please check {repo}"
        )
        click.secho(msg, **CLICK_WARNING_KWARGS)
    else:
        msg = (
            "Warning: no references.bib file detected in external content.\n"
            f"    Please check {repo}"
        )
        click.secho(msg, **CLICK_WARNING_KWARGS)
    return None
