from pathlib import Path
from typing import Any, Callable, Dict, overload

import yaml


@overload
def modify_field(
    data: dict, key: str, func: Callable, *args, **kwargs
) -> dict: ...


@overload
def modify_field(
    data: list, key: str, func: Callable, *args, **kwargs
) -> list: ...


def modify_field(
    data: dict | list, key: str, func: Callable, *args, **kwargs
) -> dict | list:
    """Modify the fields that match a given key.

    Recursively look for the fields matching a given key in a YAML-like
    mapping. Modify the matching fields by running `func` on them.

    :param data: mapping where to look for matches
    :param key: key to look for
    :param func: function to run on the matching fields
    :param args, kwargs: other positional and keyword arguments for `func`
    :return: modified mapping
    """
    if isinstance(data, dict):
        if key in data:
            return func(data, *args, **kwargs)
        else:
            return {
                k: modify_field(v, key, func, *args, **kwargs)
                for k, v in data.items()
            }
    elif isinstance(data, list):
        return [modify_field(el, key, func, *args, **kwargs) for el in data]
    return data


def load_yaml_file(
        path: str | Path, encoding: str = "utf8"
) -> Dict[str, Any]:
    """Load a yaml file file (ToC or config) as dictionary.

    :param path: file path
    :param encoding: file character encoding
    :return: parsed file
    """
    with open(path, encoding=encoding) as handle:
        data = yaml.safe_load(handle)
    return data
