# TeachBooks: Our Custom Python Package

TeachBooks has created a Python package and released it on PyPI. It can easily be used like this:
```
pip install teachbooks
```

The source code is hosted in a repository on GitHub, [github.com/teachBooks/teachbooks](https://github.com/teachBooks/teachbooks), and is accompanied by a documentation website, [teachbooks.github.io/TeachBooks/](https://teachbooks.github.io/TeachBooks/).

The features and documentation will increase with time; until then, note there are two important reasons to use the teachbooks package:
1. Use the `REMOVE-FROM-PUBLISH` feature to more easily maintain draft and published versions of your TeachBook (see {ref}`this page <remove-from-publish>` for more details).
2. Easily start and stop a local Python server to better test your book while writing (e.g., the interactive Python features require a local server to properly check certain TeachBooks features)

For case 1, the `teachbooks` package is meant to be used instead of `jupyter book build book` to build your book (it executes `jupyter book build book` for you).

Case 2 is meant to be used independently, for example, once you have successfully built a book, simply run `teachbooks serve` and open the resulting URL that is printed in the terminal. To stop the server use `teachbooks serve stop`; see {ref}`this page <setup-local-server>` for additional explanation for how to use this feature and why it is needed.

