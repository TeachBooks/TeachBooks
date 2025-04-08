This directory will be automatically populated with files when the 
documentation is built.

To build the docs make sure sphinx and the required plugins are in your current
(virtual) python environment, navigate to the docs/ directory, and do:

```sh
sphinx-build source/ _build/
```

The `docs/source/api` folder should then be populated with automatically generated
API docs.
