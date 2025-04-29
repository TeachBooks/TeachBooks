"""Utilities for external content."""

from collections.abc import Callable
from pathlib import Path
from typing import Any, overload

import yaml


@overload
def modify_field(data: dict, key: str, func: Callable, *args, **kwargs) -> dict: ...


@overload
def modify_field(data: list, key: str, func: Callable, *args, **kwargs) -> list: ...


def modify_field(
    data: dict | list, key: str, func: Callable, *args, **kwargs
) -> dict | list:
    """Modify the fields that match a given key.

    Recursively look for the fields matching a given key in a YAML-like
    mapping. Modify the matching fields by running `func` on them.

    Args:
        data: mapping where to look for matches
        key: key to look for
        func: function to run on the matching fields
        args: positional arguments for `func`
        kwargs: keyword arguments for `func`

    Returns:
        modified mapping
    """
    if isinstance(data, dict):
        if key in data:
            return func(data, *args, **kwargs)
        else:
            return {
                k: modify_field(v, key, func, *args, **kwargs) for k, v in data.items()
            }
    elif isinstance(data, list):
        return [modify_field(el, key, func, *args, **kwargs) for el in data]
    return data


def load_yaml_file(path: str | Path, encoding: str = "utf8") -> dict[str, Any]:
    """Load a yaml file file (ToC or config) as dictionary.

    Args:
        path: file path
        encoding: file character encoding

    Returns:
        parsed file
    """
    with open(path, encoding=encoding) as handle:
        data = yaml.safe_load(handle)
    return data
