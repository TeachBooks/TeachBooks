Tests
=====

Tests are executed with ``pytest`` and consist of source code for a variety of
books and pages on which the CLI tools are run. The tests are inspired by
those of Jupyter Book to help ensure that ``teachbooks`` continues to work
consistently (although this is not tested directly, except for the use of the
``jupyter-book`` command). The tests are organized in subdirectories of
``tests/`` as follows:

- ``tests/books/`` contains independent books for checking general features
- ``test/pages/`` should be used for individual pages
- ``tests/test_<...>/`` should be used for specific modules
  (e.g., ``test_external_content`` tests the external toc module)

