Introduction to TeachBooks
==========================

This Python package is primarily a wrapper around the Jupyter Book package
and is designed to facilitate usage of the platform in educational
contexts. In this case "wrapper" refers to the CLI usage: CLI commands
generally invoke `jupyter-book` commands internally; the `jupyter-book`
package is _not_ distributed within the `teachbooks` package.

The source code and function of the package is documented on this website. 
Visit the TeachBooks `website <https://teachbooks.io>`__` and `dedicated 
Manual page <https://teachbooks.io/manual/features/overview.html#teachbooks-python-package>`__
to learn more about how this package is used in an educational context.

Conventional Usage
^^^^^^^^^^^^^^^^^^

Using the teachbooks CLI in the book building process generally invokes
Jupyter Book. Many of the features in this package are then invoked in
the stages before and after this command. The process generally includes
the following steps:

1. Edit source code and prepare to build a book
2. Execute `teachbooks [OPTIONS] COMMAND [ARGS]`
3. Pre-processing step: carried out by `teachbooks`
4. Build step: book is built using `jupyter book [OPTIONS] COMMAND [ARGS]`
5. Post-processing step: carried out by `teachbooks`

Features
^^^^^^^^

- Wrapper for `jupyter-book`: pre- and post-processing steps, easy
customization of book build.
- Draft-Release workflow: take out sections not meant (yet) for
readers (students) to see.
- Local web server management: easily start a Python web server to review
changes and test features in your book.
- External Content: add material from GitHub or GitLab to your book,
by refering to it directly in the table of contents.

Installation
^^^^^^^^^^^^

`teachbooks` is `available on PyPI <https://pypi.org/project/teachbooks/>`__
and can be installed using pip:

   pip install teachbooks