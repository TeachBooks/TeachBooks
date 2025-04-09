Contributing to TeachBooks
==========================

We welcome any kind of contributions to our software, from simple
comment or question to a full fledged `pull request <https://help.github.com/articles/about-pull-requests/>`_.
Please read and follow our :doc:`Code of Conduct <code_of_conduct>`.

A contribution can be one of the following cases:

1. you have a question;
2. you think you may have found a bug (including unexpected behavior);
3. you want to make some kind of change to the code base (e.g. to fix a
   bug, to add a new feature, to update documentation).
4. you want to make a release

The sections below outline the steps in each case.

You have a question
-------------------

1. use the search functionality
   `here <https://github.com/TeachBooks/TeachBooks/issues>`__ to see
   if someone already filed the same issue;
2. if your issue search did not yield any relevant results, make a new
   issue;
3. apply the "Question" label; apply other labels when relevant.

You think you may have found a bug
----------------------------------

1. use the search functionality
   `here <https://github.com/TeachBooks/TeachBooks/issues>`__ to see
   if someone already filed the same issue;
2. if your issue search did not yield any relevant results, make a new
   issue, making sure to provide enough information to the rest of the
   community to understand the cause and context of the problem.
   Depending on the issue, you may want to include:

   - the `SHA hashcode <https://help.github.com/articles/autolinked-references-and-urls/#commit-shas>`__
     of the commit that is causing your problem;
   - some identifying information (name and version number) for dependencies you're using;
   - information about the operating system;

3. apply relevant labels to the newly created issue.

You want to make some kind of change to the code base
-----------------------------------------------------

#.  (**important**) announce your plan to the rest of the community
    *before you start working*. This announcement should be in the form
    of a (new) issue;
#.  (**important**) wait until some kind of consensus is reached about
    your idea being a good idea;
#.  if needed, fork the repository to your own Github profile and create
    your own feature branch off of the latest main commit (typically the 
    ``stable`` or ``develop`` branch). While working
    on your feature branch, make sure to stay up to date with the main
    branch by pulling in changes, possibly from the 'upstream'
    repository (follow the instructions
    `here <https://help.github.com/articles/configuring-a-remote-for-a-fork/>`__
    and `here <https://help.github.com/articles/syncing-a-fork/>`__);
#.  install package main and dev dependencies. See the :ref:`dev-environment-setup`
    below.
#.  make sure the existing documentation can still by generated without
    warnings by running ``cd docs && sphinx-build source/ _build/``.
#.   add your own tests (if necessary);
#.  update or expand the documentation; Please add `Google Style Python
    docstrings <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`__.
#.  `push <http://rogerdudler.github.io/git-guide/>`__ your feature
    branch to (your fork of) the TeachBooks repository on GitHub;
#.  create the pull request, e.g. following the instructions
    `here <https://help.github.com/articles/creating-a-pull-request/>`__.

In case you feel like you've made a valuable contribution, but you don't
know how to write or run tests for it, or how to generate the
documentation: don't let this discourage you from making the pull
request; we can help you! Just go ahead and submit the pull request, but
keep in mind that you might be asked to append additional commits to
your pull request.

.. _dev-environment-setup:

Setting up a development environment
------------------------------------

As the package and its dependencies are installed using ``pip`` in the Deploy
Book Workflow (the GitHub Action for building books), it is best to do the
same with a development environment. Begin by cloning the repository and
creating a new branch from the appropriate branch and/or commit.

The creation of the development environment should be somthing like this:

.. code-block:: shell

    conda deactivate         # Only needed if you have conda
    python3 -m venv venv     # Create a virtual environment
    source venv/bin/activate # or 'venv\Scripts\activate' on Windows
    pip install -e .[testing,docs]
    pip show teachbooks      # confirm local installation is used

Using option ``pip install -e`` is editable mode, which updates the
``teachbooks`` module in the venv as it is edited. Note that this step
can take a long time on Windows; the reason is most likely due to malware
scanners on organization-owned/managed computers. To resolve this you
should disable the "Realtime malware protection" on your machine. If that
is not possible, stop and start the installation process several times.
As you can probably already guess, the most effective solution for this
(and perhaps many of your other open source software problems) is to switch
to Linux. to avoid this). In general, the `Setuptools manual
<https://setuptools.pypa.io/en/latest/userguide/development_mode.html>`__
can be a useful reference in case you run into issues here.

The instructions above will create a venv in the root directory of the
package repository and improvements to the source code will typically
be tested by building a book. For example, testing on an existing book
with source code in ``./book/`` located outside of the teachbooks repo
will require using the relative path to the venv
``PATH_TO_TEACHBOOKS_REPO``:

.. code-block:: shell

    source PATH_TO_TEACHBOOKS_REPO/venv/bin/activate
    pip install -r requirements.txt
    teachbooks build book/
    
Alternatively, one could use one of the test books in ``./tests/``.
In fact, this is where tests should be added if making a new
contribution to the package.

You want to make a release
--------------------------

This section is for maintainers of the package.

#.  Checkout ``HEAD`` of ``stable`` branch with ``git checkout stable`` and
    ``git pull``.

#.  Determine what new version (major, minor or patch) to use. Package
    uses `semantic versioning <https://semver.org>`__.

#.  Because the stable branch is protected, you need to create a new branch
    with ``git checkout -b release-<version>``.

#.  Set new version in ``pyproject.toml`` file in project section.

#.  Update ``CHANGELOG.md`` with changes between current and new version.

#.  Make sure all tests passed by running ``pytest``.

#.  Commit & push changes to GitHub.

#.  Create a pull request, review it, wait for actions to be green and
    merge the pull request.

#.  Wait for `GitHub
    actions <https://github.com/TeachBooks/TeachBooks/actions?query=branch%3Astable+>`__
    on stable branch to be completed and green.

#.  Create a `GitHub
    release <https://github.com/TeachBooks/TeachBooks/releases/new>`__

    -  Use version as title and tag version.
    -  As description use intro text from README.md (to give context) and
       changes from CHANGELOG.md

#.  Verify

    1. Has `stable
       ReadTheDocs <https://teachbooks.readthedocs.io/en/stable/>`__
       been updated?
    2. Has the `Github publish
       action <https://github.com/TeachBooks/TeachBooks/actions/workflows/publish.yml>`__
       successfully uploaded the archives to
       `PyPI <https://pypi.org/project/teachbooks/>`__?
    3. Can new version be installed with pip using
       ``pip install teachbooks==<new version>``?

#.  Celebrate

Releases and Versioning
-----------------------

Semantic numbering is used: `vA.B.C`, where patches advance `C` and minor
releases advance `B`. `Releases in the GitHub Repository
<https://github.com/TeachBooks/TeachBooks/releases>`__ deploy automatically
to [PyPI](https://pypi.org/project/teachbooks/) once a tag is created and
the `pyproject.toml` file is updated with the new version number. Minor
releases will be merged into the `stable` branch (including those below
`v1.0.0`); patches may be incorporated in `develop` or `stable`.

As described above, a Pull Request should be created when making a
contribution. A draft Pull Request may be set up between the ``develop`` and
``stable`` branches to preview updates for the next minor or major release.

If a release must be available on PyPI but it is not desired for it to be
available as the primary release, use the numbering `vA.B.Cbn`, where `n`
is an increasing number starting from 1. The specific version can be installed
via pip using `pip install teachbooks==A.B.Cbn`. A tag defining this type of
release may be used on any branch.