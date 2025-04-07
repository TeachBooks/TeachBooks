.. TeachBooks documentation master file, created by
   sphinx-quickstart on Mon Apr 22 11:34:16 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TeachBooks Documentation: Welcome!
==================================

This Python package is primarily a wrapper around the Jupyter Book package
and is designed to facilitate usage of the platform in educational
contexts. In this case "wrapper" refers to the CLI usage: CLI commands
generally invoke `jupyter-book` commands internally; the `jupyter-book`
package is _not_ distributed within the `teachbooks` package.

The source code and function of the package is documented on this website. 
Visit the TeachBooks `website <https://teachbooks.io>`__` and `dedicated 
Manual page <https://teachbooks.io/manual/features/overview.html#teachbooks-python-package>`__
to learn more about how this package is used in an educational context.

Contents
^^^^^^^^
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro
   cli/cli
   api
   external
   contributing
   tests