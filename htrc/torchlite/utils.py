import math
from typing import Iterable, Any, TypeVar

from ruamel.yaml import YAML
#from htrc.torchlite.http_client import http

T = TypeVar('T')
U = TypeVar('U')


def make_set(value: T | list[T] | None) -> set[T]:
    if value is None:
        return set()
    elif isinstance(value, list):
        return set(value)
    else:
        return {value}


def make_list(value: T | list[T] | None) -> list[T]:
    if value is None:
        return []
    elif isinstance(value, list):
        return value
    else:
        return [value]


def flatten(collection: Iterable[list[T]]) -> list[T]:
    flat_list = []
    for lst in collection:
        if lst is None:
            continue
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


def make_batches(lst: list[T], chunk_size: int) -> list[list[T]]:
    return [lst[i * chunk_size:(i + 1) * chunk_size] for i in range(math.ceil(len(lst) / chunk_size))]


def parse_value(v: T | list[T] | None, field: str = 'name') -> U | list[U] | None:
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


#async def load_yaml(url: str) -> dict:
#    response = await http.get(url)
#    return YAML().load(response.content)
