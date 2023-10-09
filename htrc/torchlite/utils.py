import math
from typing import Iterable, Any, TypeVar


def make_set(value: str | list[str] | None) -> set[str]:
    return set(value) if value is not None else set()


def make_list(value: dict | list[dict] | None) -> list[dict]:
    if value is None:
        return []
    elif isinstance(value, dict):
        return [value]
    else:
        return value


def flatten(collection: Iterable[list]) -> list:
    flat_list = []
    for lst in collection:
        flat_list.extend(lst)

    return flat_list


def parse_dict(d: dict, path: str, raise_if_not_exist: bool = False) -> Any | None:
    for prop in path.split('.'):
        d = d.get(prop)
        if d is None:
            if raise_if_not_exist:
                raise KeyError(prop)
            else:
                return None
    return d


def make_batches(l: list, chunk_size: int) -> list[list]:
    return [l[i * chunk_size:(i + 1) * chunk_size] for i in range(math.ceil(len(l) / chunk_size))]


T = TypeVar('T')
U = TypeVar('U')


def parse_value(v: T | list[T] | None, field: str = 'name') -> U | list[U] | None:
    result = None
    if isinstance(v, list):
        result = [
            x for e in v
            if (x := e.get(field) if isinstance(e, dict) else getattr(e, field, None)) is not None
        ]
        result = result or None
    elif isinstance(v, dict):
        result = v.get(field)
    else:
        result = getattr(v, field, None)

    return result


def sanitize(data):
    if isinstance(data, str):
        return data.strip() or None
    elif isinstance(data, dict):
        return {k: sanitize(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [v for e in data if (v := sanitize(e)) is not None] or None
    else:
        return data
