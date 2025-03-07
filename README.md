# TeachBooks Package: Jupyter Book Wrapper

This Python package is primarily a wrapper around the Jupyter Book package and is designed to facilitate usage of the platform in educational contexts. In this case "wrapper" refers to the CLI usage: CLI commands generally invoke `jupyter-book` commands internally; the `jupyter-book` package is _not_ distributed within the `teachbooks` package.

The source code and function of the package is documented on a Sphinx-built website: [teachbooks.io/TeachBooks/](https://teachbooks.io/TeachBooks/). Visit the TeachBooks [website](https://teachbooks.io) and [manual](https://teachbooks.io/manual) to learn more about how this package is used in an educational context.

The package is currently [available on PyPI](https://pypi.org/project/teachbooks/) only and can be installed as follows:

```
pip install teachbooks
```

## Primary Features

Key features include:
- `jupyter-book` wrapper, pre- and post-processing steps
- draft/release workflow
- manage a local Python http server

### Jupyter Book wrapper and processing steps

Using the teachbooks CLI in the book building process generally invokes Jupyter Book. Many of the features in this package are then invoked in the stages before and after this command. The process generally includes the following steps:

1. Edit source code and prepare to build a book
2. Execute `teachbooks [OPTIONS] COMMAND [ARGS]`
3. Pre-processing step: carried out by `teachbooks`
4. Build step: book is built using `jupyter book [OPTIONS] COMMAND [ARGS]`
5. Post-processing step: carried out by `teachbooks`

## Updates and Improvements

Expect frequent updates to the package as patches and minor releases until further notice. We expect to release `v1.0.0` in Spring, 2025. Update the package in your local environment using using `pip install --upgrade teachbooks`. Visit the setup chapter of the [TeachBooks Manual](https://teachbooks.io/manual/installation-and-setup/overview.html) for more information.

To contribute, create a fork and open a pull request to the (default) `develop` branch. An open pull request "Next release vA.B.C" should be created between `develop` and `stable` to illustrate changes in the next minor release.

Semantic numbering is used: `vA.B.C`, where patches advance `C` and minor releases advance `B`. [Releases in the GitHub Repository](https://github.com/TeachBooks/TeachBooks/releases) deploy automatically to [PyPI](https://pypi.org/project/teachbooks/) once a tag is created and the `pyproject.toml` file is updated with the new version number. Minor releases will be merged into the `stable` branch (including those below `v1.0.0`); patches may be incorporated in `develop` or `stable`. 

If a release must be available on PyPI but it is not desired for it to be available as the primary release, use the numbering `vA.B.Cbn`, where `n` is an increasing number starting from 1. The specific version can be installed via pip using `pip install teachbooks==A.B.Cbn`.

## Acknowledgements

This package received financial support from the Civil Engineering and Geosciences faculty at Delft University of Technology in the Netherlands via Education Innovation Projects, [MUDE](https://mude.citg.tudelft.nl) and direct financial support of Jupyter Book applications in education by the CEG faculty. The project also received funding from the TU Delft Library at the end of 2024.

The first version of this package was created and released by Caspar Jungbacker in Spring, 2024 and has since been primarily maintained by TeachBooks contributors and MUDE the Student Army.

## License

This software will most likely be licensed with a BSD 3-clause license, which aligns with similar Python packages (e.g., Jupyter Book). However, the license file is not yet included with this repository as we are currently in the process of reviewing Copyright status.

## Development

New features and improvements are incorporated via pull requests to the (default) `develop` branch. 

### Documentation Website

The [documentation for this package](https://teachbooks.io/teachbooks) is built using Sphinx and @pradyunsg's Furo; use the [Furo documentation](https://pradyunsg.me/furo/#) as a reference when updating the documentation site.

### Development Setup

_Work in progress. This is a quick summary of the process used in [PR 44](https://github.com/TeachBooks/TeachBooks/pull/44), which could become the "standard" development setup. See [TeachBooks Discussion 49](https://github.com/TeachBooks/TeachBooks/discussions/49) for a more thorough overview and/or to make suggestions!_

The steps and packages are chosen to match our GitHub Actions workflows as closely as possible, which use `pip`. 

```
conda deactivate
<path to your>\python -m venv venv
venv\Scripts\activate
pip install -e .
```

Check that the local installation worked by running `pip show teachbooks`. For running tests, install dependencies listed in `pyproject.toml`.
