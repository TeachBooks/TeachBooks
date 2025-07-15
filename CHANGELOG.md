# Change Log

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).
Formatted as described on [https://keepachangelog.com](https://keepachangelog.com/en/1.0.0/).

## Unreleased

## 0.2.2 - 2025-07-15

### Fixed

- Nested `external:` entries in the table of content are now parsed correctly ([#108](https://github.com/TeachBooks/TeachBooks/pull/108)).
- `LICENSE.txt` and `LICENSE.rst` files are now also checked when cloning external content ([#110](https://github.com/TeachBooks/TeachBooks/pull/110)).

## 0.2.1 - 2025-05-02

### Added

- admonitions which will automatically be added at the top of external content pages ([#96](https://github.com/TeachBooks/TeachBooks/pull/96)).
  - The admonition location can be configured (either at top of page or in the right margin) ([#98](https://github.com/TeachBooks/TeachBooks/pull/98)).
  - The color of the admonition can be configured ([#98](https://github.com/TeachBooks/TeachBooks/pull/98)).
- Automatically generated API docs to the package documentation ([#89](https://github.com/TeachBooks/TeachBooks/pull/89)).
- 

## 0.2.0 - 2025-04-07

This release introduces an exciting new feature: automatically including external content in your book!

### Added

- A new way to include external content in your books. You can now refer to other books published on github/gitlab. For more info [see the documentation page](https://teachbooks.readthedocs.io/latest/external.html) and the dedicated [TeachBooks Manual page](https://teachbooks.io/manual/features/external_toc.html) ([#59](https://github.com/TeachBooks/TeachBooks/pull/59)).
- Documentation for the entire package is provided by via Read the Docs: [teachbooks.readthedocs.io](https://teachbooks.readthedocs.io/latest/)
- A license is now provided (MIT)
- A waiver is added clarifying that TeachBooks is the copyright holder, allowing contributions from the community to be more straightforward
- added Linkspector to verify URL's in documentation
- A changelog

## 0.2.0b1 - 2025-03-07

A temporary release for testing a GUI prior to the package being ready. Also required waiting for the Deploy Book Workflow and Manual to be updated and checked to understand the impact of changing the package to the books that are currently active and using the workflow.

### Added

- a new way to include external content in your books. You can now refer to other books published on github/gitlab. For more info [see the documentation page](https://teachbooks.readthedocs.io/latest/external.html) ([#59](https://github.com/TeachBooks/TeachBooks/pull/59)).

## 0.1.0 - 2024-12-10

See GitHub.
