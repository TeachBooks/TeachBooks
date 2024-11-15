# TeachBooks package: Exclude parts of book from released book and local Python server

TeachBooks has created a Python package and released it on PyPI. It can easily be used like this:

```
pip install teachbooks
```

The source code is hosted in a repository on GitHub, [github.com/teachBooks/teachbooks](https://github.com/teachBooks/teachbooks), and is accompanied by a documentation website, [teachbooks.github.io/TeachBooks/](https://teachbooks.github.io/TeachBooks/).

The features and documentation will increase with time; until then, note there are two important reasons to use the teachbooks package: remove development pages from released book and start a local Python server.

## Remove development pages from released book
Use the `REMOVE-FROM-RELEASE` feature to more easily maintain development and released versions of your TeachBook. This removes any sections surrounded by REMOVE-FROM-RELEASE tags from _config.yml and _toc.yml. This allows you to viewing a work-in-progress while preventing students from seeing it is available if those branches are merged into the release version. For example, pages in a developed book (e.g., `dev` branch) can be manually stripped out of the table of contents when a merge request from `dev` to `release` is made. This prevents the page being included in the released book. Pages marked with this feature are still visible in the `dev` book. Lines tagged in the configuration file `_config.yml` can be used in exactly the same manner. The tag is applied as follows:

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

## Local Python server
Easily start and stop a local Python server to better test your book while writing (e.g., the interactive Python features require a local server to properly check certain TeachBooks features). Some features like interactive python code and Grasple only work when a webserver serves the HTML content for a book. Rather than building the book in your repository and updating the website on the internet, you can use a local webserver to view the book:
1. Make sure you have the TeachBooks Python package installed (e.g., `pip install teachbooks`)
2. Start a server from the command line with: `teachbooks serve`
3. The command line output will return the URL where you can access your book
4. You should reload the page if you are editing and rebuilding the book. You can try `CTRL+R` `ctrl`+`F5`. If this does not work, on Chrome try right-clicking somewhere on the page, select \"Inspect\", open the \"Network\" tab, then reload with `CTRL+R`. 
5. All interactive features like the Grasple/H5p iframe exercises, Sphinx-thebe python interactivity and HTML/Javascript elements should now work as well.
6. When you no longer need the server, simply run `teachbooks serve stop`

### How to create a local server without the TeachBooks package

Here is how to set up a local server with only standard Python libraries:

1. Start a server from the command line with: `python -m http.server -b 127.0.0.1` (add ` &` if you want to keep using the terminal for other tasks).
2. Port 8000 is usually used by default, but depending on your OS it will tell you in the output.
3. To visit your site, just enter the address in your web browser, followed by a colon, and then the port number. By default, that would be: `127.0.0.1:8000`.
4. You will get a website that looks like a file browser, to visit your site just navigate to `book/_build/html/` (if you've started this command from this folder you see the book immediately)


## Contribute
This tool's repository is stored on [GitHub](https://github.com/TeachBooks/TeachBooks). The `README.md` of the branch `docs-book` is also part of the [TeachBooks manual](https://teachbooks.tudelft.nl/jupyter-book-manual/external/TeachBooks/README.html) as a submodule. If you'd like to contribute, you can create a fork and open a pull request on the [GitHub repository](https://github.com/TeachBooks/TeachBooks). To update the `README.md` shown in the TeachBooks manual, create a fork and open a merge request for the [GitLab repository of the manual](https://gitlab.tudelft.nl/interactivetextbooks-citg/jupyter-book-manual). If you intent to clone the manual including its submodules, clone using: `git clone --recurse-submodules git@gitlab.tudelft.nl:interactivetextbooks-citg/jupyter-book-manual.git`.
