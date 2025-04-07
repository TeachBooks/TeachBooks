Introduction to TeachBooks
==========================

Conventional Usage
^^^^^^^^^^^^^^^^^^

Using the teachbooks CLI in the book building process generally invokes
Jupyter Book. Many of the features in this package are then invoked in
the stages before and after this command. The process generally includes
the following steps:

1. Edit source code and prepare to build a book
2. Execute ``teachbooks [OPTIONS] COMMAND [ARGS]``
3. Pre-processing step: carried out by ``teachbooks``
4. Build step: book is built using ``jupyter book [OPTIONS] COMMAND [ARGS]``
5. Post-processing step: carried out by ``teachbooks``

Features
^^^^^^^^

- Wrapper for ``jupyter-book``: pre- and post-processing steps, easy
  customization of book build.
- Draft-Release workflow: take out sections not meant (yet) for
  readers (students) to see.
- Local web server management: easily start a Python web server to review
  changes and test features in your book.
- External Content: add material from GitHub or GitLab to your book,
  by refering to it directly in the table of contents.

Installation
^^^^^^^^^^^^

``teachbooks`` is `available on PyPI <https://pypi.org/project/teachbooks/>`__
and can be installed using pip:


.. code-block:: shell

   pip install teachbooks