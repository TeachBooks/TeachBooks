External content from GitHub/GitLab
===================================

TeachBooks includes an 'external content' processor, where you can refer to meterial
hosted on GitHub or GitLab, which will be retrieved on-the-fly during the build process.

This feature works consistently when using draft or release build strategies.

Example
^^^^^^^

Modify your ``_toc.yml`` file by adding an ``external`` entry:

.. code-block:: yaml
    :emphasize-lines: 8

    format: jb-book
    root: intro.md

    parts:
    - caption: Contents
        chapters:
        - file: references.md
        - external: https://github.com/TeachBooks/manual/blob/v1.1.1/book/contact.md


Upon running ``teachbooks build book/``, the following will happen:

#. The table of content will be parsed to find any "external" keys.
#. The git repositories corresponding to the "external" keys will be cloned into a subdirectory `_git/`.
#. The licenses of the repositories are validated. If no (open) license is found, an error is raised.
#. The ``requirements.txt`` files of the external repositories are checked for any missing values or conflicts.
   If any missing values or conflicts are found, a warning is raised during the build process.
#. The ``_config.yml`` files of the external repositories are checked for any missing plugins or MyST extensions.
   If any missing plugins/extensions are found, a warning is raised during the build process.
#. The external repositories are checked for any ``references.bib`` files.
   These are merged together with the main book's ``references.bib`` file.
#. A new table of contents is generated (``local_toc.yml```) which refers to the locally cloned content.

Upon running ``teachbooks clean book/``, the `_git/` subdirectory will be removed 
(along with the build artifacts).

Notes
^^^^^

The external content links should be formatted like this:

* \https://github.com/**ORGANIZATION**/**REPOSITORY**/blob/**TAG**/path/to/file.md
* \https://gitlab.domainname.tld/**GROUP**/**PROJECT**/-/blob/**TAG**/path/to/file.md
* or \https://gitlab.domainname.tld/**GROUP**/**SUBGROUP**/**PROJECT**/blob/**TAG**/path/to/file.md

Instead of a ``tag``, it is possible to refer to a branch as well. However, this content
is not guaranteed to stay the same (i.e., if the branch is modified with additional commits). 
Therefore it's best practice to only refer to tags associated with releases, as this will 
guarantee that the content in your book only changes when you explicitly update the tag.
