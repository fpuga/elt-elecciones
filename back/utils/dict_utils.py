from collections.abc import MutableMapping


def _flatten_dict_gen(d, parent_key, sep):
    for k, v in d.items():
        new_key = k
        if sep:
            new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            yield from flat_nested_recursively(v, new_key, sep=sep).items()
        else:
            yield new_key, v


def flat_nested_recursively(d: MutableMapping, parent_key: str = "", sep: str = "."):
    """Flats all nested (and subnested) dicts.

    Doesn't modify the original dict.

    if `sep` is falsy does not prefix nested keys. Take care with this as coincident keys
    will overwrite the values.

    https://www.freecodecamp.org/news/how-to-flatten-a-dictionary-in-python-in-4-different-ways/
    """
    return dict(_flatten_dict_gen(d, parent_key, sep))
