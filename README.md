# TeachBooks Package: Jupyter-Book Wrapper for Pre- and Postprocessing

```{admonition} User types
:class: tip
This section is useful for user type 4-5.
```

The package is a CLI tool that primarily provides a wrapper around the Jupyter Book package. In this case "wrapper" refers to the CLI usage: CLI commands generally invoke `jupyter-book` commands internally; the `jupyter-book` package is _not_ distributed within the `teachbooks` package.

The source code and function of the package is documented on a Sphinx-built website: [teachbooks.io/TeachBooks/](https://teachbooks.io/TeachBooks/).

## Primary Features and Installation

Key features (described below) include:
- `jupyter-book` wrapper, pre- and post-processing steps
- draft/release workflow
- manage a local Python http server

### Installation

The package is currently only available on PyPI and can be installed as follows:

```
pip install teachbooks
```

### Jupyter Book wrapper and processing steps

Using the teachbooks CLI in the book building process generally invokes Jupyter Book. Many of the features in this package are then invoked in the stages before and after this command. The process generally includes the following steps:

1. Edit source code and prepare to build a book
2. Execute `teachbooks [OPTIONS] COMMAND [ARGS]`
3. Pre-processing step: carried out by `teachbooks`
4. Build step: book is built using `jupyter book [OPTIONS] COMMAND [ARGS]`
5. Post-processing step: carried out by `teachbooks`

### Draft/Release Workflow

Often it is necessary to prepare, review and edit materials in parallel to material that is currently being used by students, or another target audience. This workflow enables an author to easily maintain separate versions of a book without having to repeatedly comment out lines of a table of contents or page when building different versions. It is also easy to implement in CI/CD settings.  

The workflow is enabled by a `teachbooks` CLI feature that identifies and removes any lines from the files `_config.yml` and `_toc.yml` file that are surrounded by `REMOVE-FROM-RELEASE` tags.

For example, pages in a developed book (e.g., `dev` branch) can be manually stripped out of the table of contents when a merge request from `dev` to `release` is made. This prevents the page being included in the released book. Pages marked with this feature are still visible in the `dev` book. Lines tagged in the configuration file `_config.yml` can be used in exactly the same manner. The tag is applied as follows:

```
format: jb-book
root: intro

parts:
  - caption: ...
    chapters: 
    - file: ...
      ...
# START REMOVE-FROM-PUBLISH
    - file: files_to_remove
# END REMOVE-FROM-PUBLISH
```

There is no limit to the number of stripped sections, they can be sequential and indentation does not matter.

To invoke the tag and remove content during the book build process, use the following optional argument when building the book with the `teachbooks` package:

```
teachbooks build --publish book
```

Note that `teachbooks build book` would build a book without stripping the tagged lines, just as `jupyter-book build book` would.

Additional options like used in jupyterbook (`--all` for example) can be added to the command similary as with the `jupyter-book` command.

### Local Python server

```{admonition} User types
:class: tip
This section is useful for user type 5.
```

Easily start and stop a local Python server to better test your book while writing (e.g., the interactive Python features require a local server to properly check certain TeachBooks features). Some features like interactive python code and Grasple only work when a webserver serves the HTML content for a book. Rather than building the book in your repository and updating the website on the internet, you can use a local webserver to view the book:

1. Make sure you have the TeachBooks Python package installed (e.g., `pip install teachbooks`)
2. Start a server from the command line with: `teachbooks serve`
3. The command line output will return the URL where you can access your book
4. You should reload the page if you are editing and rebuilding the book. You can try `CTRL+R` `ctrl`+`F5`. If this does not work, on Chrome try right-clicking somewhere on the page, select \"Inspect\", open the \"Network\" tab, then reload with `CTRL+R`. 
5. All interactive features like the Grasple/H5p iframe exercises, Sphinx-thebe python interactivity and HTML/Javascript elements should now work as well.
6. When you no longer need the server, simply run `teachbooks serve stop`

## Acknowledgements

This package received financial support from the Civil Engineering and Geosciences faculty at Delft University of Technology in the Netherlands via Education Innovation Projects, [MUDE](https://mude.citg.tudelft.nl) and direct financial support of Jupyter Book applications in education. The project also received funding from the TU Delft Library at the end of 2024.

The first version of this package was created and released by Caspar Jungbacker in Spring, 2024 and has since been primarily maintained by the TeachBooks and MUDE Student Army. 

## Contribute

This tool's repository is stored on [GitHub](https://github.com/TeachBooks/TeachBooks). The `README.md` of the branch `docs-book` is also part of the [TeachBooks manual](https://teachbooks.io/manual/external/TeachBooks/README.html) as a submodule. If you'd like to contribute, you can create a fork and open a pull request on the [GitHub repository](https://github.com/TeachBooks/TeachBooks). To update the `README.md` shown in the TeachBooks manual, create a fork and open a merge request for the [GitHub repository of the manual](https://github.com/TeachBooks/manual). If you intent to clone the manual including its submodules, clone using: `git clone --recurse-submodulesgit@github.com:TeachBooks/manual.git`.

### Documentation Website

The documentation page for this package is built using Sphinx and @pradyunsg's Furo; use the [Furo documentation](https://pradyunsg.me/furo/#) as a reference when updating the documentation site.