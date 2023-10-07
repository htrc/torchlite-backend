
def make_set(value: str | list[str] | None) -> set[str]:
    return set(value) if value is not None else set()


def make_list(value: dict | list[dict] | None) -> list[dict]:
    if value is None:
        return []
    elif isinstance(value, dict):
        return [value]
    else:
        return value


def parse_value(v: dict | list[dict] | None, field: str = 'name') -> str | list[str] | None:
    result = None
    if isinstance(v, list):
        result = [x for e in v if (x := e.get(field)) is not None] or None
    elif isinstance(v, dict):
        result = v.get(field)

    return result
