"""Teachbooks release workflow."""

import os
import re
from pathlib import Path


def make_release(sourcedir: Path, processed_toc: Path = None) -> tuple[Path, Path, Path]:
    """Pre-process files in a Jupyter Book directory."""
    # Make hidden directory that will contain the cleaned-up files
    workdir = sourcedir.joinpath(".teachbooks", "release")

    if not os.path.exists(workdir):
        os.makedirs(workdir)

    # Process config files
    clean_yaml(sourcedir.joinpath("_config.yml"), workdir.joinpath("_config.yml"))
    
    # For ToC, use processed version if provided, otherwise use original
    toc_source = processed_toc if processed_toc else sourcedir.joinpath("_toc.yml")
    clean_yaml(toc_source, workdir.joinpath("_toc.yml"))

    # Process all files in the source directory
    for root, _, files in os.walk(sourcedir):
        for file in files:
            source_file = Path(root) / file
            # Skip hidden directories and files
            if any(part.startswith('.') for part in source_file.relative_to(sourcedir).parts):
                continue
            
            # Skip config files that are already processed above
            if file in ['_config.yml', '_toc.yml'] and source_file.parent == sourcedir:
                continue
                
            # Calculate relative path from sourcedir
            rel_path = source_file.relative_to(sourcedir)
            output_file = workdir / rel_path
            
            # Create output directory if it doesn't exist
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Process the file based on its extension
            if file.endswith('.md'):
                clean_md(source_file, output_file)
            elif file.endswith('.ipynb'):
                clean_ipynb(source_file, output_file)
            else:
                # Copy all other files (images, CSS, etc.) as-is
                import shutil
                shutil.copy2(source_file, output_file)

    return workdir.joinpath("_config.yml"), workdir.joinpath("_toc.yml"), workdir


def copy_ext(sourcedir: Path) -> None:
    """Copy _ext/ to support APA in release [TEMPORARY]."""
    # Make hidden directory that will contain the cleaned-up files
    ext_dir = sourcedir.joinpath("_ext")
    workdir = sourcedir.joinpath(".teachbooks", "release")

    if not os.path.exists(workdir):
        os.makedirs(workdir)

    try:
        for root, dirs, files in os.walk(ext_dir):
            for _dir in dirs:
                os.makedirs(
                    workdir.joinpath(
                        "_ext", Path(root).relative_to(ext_dir).joinpath(_dir)
                    ),
                    exist_ok=True,
                )
            for file in files:
                src_file = Path(root).joinpath(file)
                dest_file = workdir.joinpath(
                    "_ext", Path(root).relative_to(ext_dir).joinpath(file)
                )
                os.makedirs(dest_file.parent, exist_ok=True)
                with open(src_file, "rb") as fsrc, open(dest_file, "wb") as fdst:
                    fdst.write(fsrc.read())
        print("Copied _ext/ directory successfully.")
    except:  # noqa: E722 (TODO: isolate specific exception, or re-raise error.)
        print("Error copying _ext/ directory.")


def clean_yaml(path_source: str | Path, path_output: str | Path) -> None:
    """Removes marked sections from a yaml file.

    A marked section can be:
        - ``# <START|END> REMOVE-FROM-PUBLISH``
        - or ``# <START|END> REMOVE-FROM-RELEASE``

    Does not require a specific indentation and can be used an
    unlimited number of times in the ``*.yml`` file. Commonly
    applied to ``_toc.yml`` and ``_config.yml`` files of a book.

    Example:
        To remove sub_page_2 and sub_page_3 from publishing::

            - file: subdirectory_1/intro_page
            sections:
            - file: subdirectory_1/sub_page_1
            # START REMOVE-FROM-PUBLISH
            - file: subdirectory_1/sub_page_2
            # END REMOVE-FROM-PUBLISH
            # START REMOVE-FROM-RELEASE
            - file: subdirectory_1/sub_page_3
            # END REMOVE-FROM-RELEASE
            - file: subdirectory_2/intro_page

    """
    with open(path_source, encoding="utf8") as f:
        yaml_source = f.read()

    # Regex to remove both PUBLISH and RELEASE tags
    re_pub_release = (
        r"# START REMOVE-FROM-(PUBLISH|RELEASE)(.|\n)*?"
        r"# END REMOVE-FROM-(PUBLISH|RELEASE)"
    )
    yaml_output = re.sub(re_pub_release, "", yaml_source)

    with open(path_output, mode="w", encoding="utf8") as f:
        f.write(yaml_output)

def clean_md(path_source: str | Path, path_output: str | Path) -> None:
    """Removes marked sections from a markdown file.

    A marked section can be:
        - ``% START REMOVE-FROM-PUBLISH``
        - ``% END REMOVE-FROM-PUBLISH``
        - ``% START REMOVE-FROM-RELEASE``
        - ``% END REMOVE-FROM-RELEASE``

    Can be used an unlimited number of times in the ``*.md`` file.

    """
    with open(path_source, encoding="utf8") as f:
        md_source = f.read()

    # Regex to remove both PUBLISH and RELEASE tags
    re_pub_release = (
        r"% START REMOVE-FROM-(PUBLISH|RELEASE)(.|\n)*?"
        r"% END REMOVE-FROM-(PUBLISH|RELEASE)"
    )
    md_output = re.sub(re_pub_release, "", md_source)

    with open(path_output, mode="w", encoding="utf8") as f:
        f.write(md_output)

def clean_ipynb(path_source: str | Path, path_output: str | Path) -> None:
    """Removes marked sections from a Jupyter Notebook file.

    A marked section can be:
        - ``# START REMOVE-FROM-PUBLISH`` / ``# END REMOVE-FROM-PUBLISH`` (for code cells)
        - ``# START REMOVE-FROM-RELEASE`` / ``# END REMOVE-FROM-RELEASE`` (for code cells)
        - ``% START REMOVE-FROM-PUBLISH`` / ``% END REMOVE-FROM-PUBLISH`` (for markdown cells)
        - ``% START REMOVE-FROM-RELEASE`` / ``% END REMOVE-FROM-RELEASE`` (for markdown cells)

    Does not require a specific indentation and can be used an
    unlimited number of times in the ``*.ipynb`` file. Commonly
    applied to Jupyter Notebook files of a book.

    """
    import json
    
    with open(path_source, encoding="utf8") as f:
        notebook = json.load(f)
    
    # Process each cell to remove marked sections
    for cell in notebook.get('cells', []):
        if 'source' in cell and cell['source']:
            # Join source lines into a single string for processing
            source_text = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            
            # Use regex to remove marked sections - handle both # and % comments
            re_remove = r'[#%] START REMOVE-FROM-(?:PUBLISH|RELEASE).*?[#%] END REMOVE-FROM-(?:PUBLISH|RELEASE)'
            cleaned_text = re.sub(re_remove, '', source_text, flags=re.DOTALL)
            
            # Convert back to original format
            if isinstance(cell['source'], list):
                # Split back into lines and add newlines appropriately
                lines = cleaned_text.split('\n')
                cell['source'] = [line + '\n' for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
            else:
                cell['source'] = cleaned_text
    
    # Save the modified notebook
    with open(path_output, mode="w", encoding="utf8") as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)