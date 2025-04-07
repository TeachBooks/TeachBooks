# TeachBooks Package: Jupyter Book Wrapper

This Python package is primarily a wrapper around the Jupyter Book package and is designed to facilitate usage of the platform in educational contexts. In this case "wrapper" refers to the CLI usage: CLI commands generally invoke `jupyter-book` commands internally; the `jupyter-book` package is _not_ distributed within the `teachbooks` package.

The source code and function of the package is documented at [teachbooks.readthedocs.io](https://teachbooks.readthedocs.io). Visit the TeachBooks [website](https://teachbooks.io) and [dedicated Manual page](https://teachbooks.io/manual/features/overview.html#teachbooks-python-package) to learn more about how this package is used in an educational context.

## Updates and Improvements

Expect frequent updates to the package as patches and minor releases until further notice. We expect to release `v1.0.0` in Spring, 2025. Update the package in your local environment using using `pip install --upgrade teachbooks`.

Contributions are ideally made via a fork and pull request to the (default) `develop` branch (see the project [Documentation](https://teachbooks.readthedocs.io) for detailed instructions).

## Documentation Website

The documentation for this package is built using Sphinx and @pradyunsg's Furo; use the [Furo documentation](https://pradyunsg.me/furo/#) as a reference when updating the documentation site.

The Read the Docs website [teachbooks.readthedocs.io](https://teachbooks.readthedocs.io) maintains documentation for each tagged release beginning with `v0.2.0`. The documentation website is also deployed from GitHub Pages from the `stable` branch and can be accessed at [teachbooks.io/TeachBooks/](https://teachbooks.io/TeachBooks/). This should remain identical to the "latest" (default) Read the Docs documentation page as long as the most recent tagged release is on branch `stable`.

## Acknowledgements

This package received financial support from the Civil Engineering and Geosciences faculty at Delft University of Technology in the Netherlands via Education Innovation Projects, [MUDE](https://mude.citg.tudelft.nl) and direct financial support of Jupyter Book applications in education by the CEG faculty. The project also received funding from the TU Delft Library at the end of 2024. Bart Schilperoort of the Netherlands eScience Center implemented the external contents module and also provided critical advice on the journey to `v1.0.0`.

The first version of this package was created and released by Caspar Jungbacker in Spring, 2024 and has since been primarily maintained by a variety of TeachBooks contributors. 