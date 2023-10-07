import json

from .models.dashboard import FilterSettings
from .models.workset import WorksetSummary, VolumeMetadata, WorksetInfo

with open('data/worksets.json', 'r') as f:
    arr = json.load(f)
    worksets: dict[str, WorksetSummary] = {w['id']: WorksetSummary(**w) for w in arr}


def sanitize(v: str | list[str] | None) -> str | list[str] | None:
    if isinstance(v, str):
        return v.strip() or None

    if isinstance(v, list):
        return [x for e in v if (x := sanitize(e)) is not None] or None

    return v


def parse_value(v: dict | list[dict] | None, field: str = 'name') -> str | list[str] | None:
    result = None
    if isinstance(v, list):
        result = [x for e in v if (x := sanitize(e.get(field))) is not None] or None
    elif isinstance(v, dict):
        result = sanitize(v.get(field))

    return result


def parse_volume_meta(vol: dict) -> VolumeMetadata:
    meta = vol['metadata']
    return VolumeMetadata(
        htid=sanitize(vol['htid']),
        title=sanitize(meta['title']),
        pub_date=sanitize(meta.get('pubDate')),
        genre=sanitize(meta['genre']),
        type_of_resource=sanitize(meta['typeOfResource']),
        category=sanitize(meta.get('category')),
        contributor=parse_value(meta.get('contributor')),
        publisher=parse_value(meta.get('publisher')),
        access_rights=sanitize(meta['accessRights']),
        pub_place=parse_value(meta.get('pubPlace')),
        language=sanitize(meta.get('language')),
        source_institution=parse_value(meta['sourceInstitution']),
    )


def get_workset_info(workset_id: str) -> WorksetInfo:
    with open(f'data/{workset_id}.json', 'r') as f:
        data = json.load(f)

    volumes = [parse_volume_meta(vol) for vol in data['data']]
    ws = worksets[workset_id]

    return WorksetInfo.model_construct(**ws.model_dump(), volumes=volumes)


def make_set(value: str | list[str] | None) -> set[str]:
    return set(value) if value is not None else set()


def apply_filters(workset_info: WorksetInfo, filters: FilterSettings) -> WorksetInfo:
    filtered_volumes = []
    for volume_meta in workset_info.volumes:
        if filters.title and volume_meta.title not in filters.title:
            continue
        if filters.pub_date and volume_meta.pub_date not in filters.pub_date:
            continue
        if filters.genre and not make_set(volume_meta.genre).intersection(filters.genre):
            continue
        if filters.type_of_resource and volume_meta.type_of_resource not in filters.type_of_resource:
            continue
        if filters.category and not make_set(volume_meta.category).intersection(filters.category):
            continue
        if filters.contributor and not make_set(volume_meta.contributor).intersection(filters.contributor):
            continue
        if filters.publisher and not make_set(volume_meta.publisher).intersection(filters.publisher):
            continue
        if filters.access_rights and volume_meta.access_rights not in filters.access_rights:
            continue
        if filters.pub_place and not make_set(volume_meta.pub_place).intersection(filters.pub_place):
            continue
        if filters.language and not make_set(volume_meta.language).intersection(filters.language):
            continue
        if filters.source_institution and volume_meta.source_institution not in filters.source_institution:
            continue

        filtered_volumes.append(volume_meta)

    return WorksetInfo.model_construct(**{**workset_info.model_dump(), 'volumes': filtered_volumes})
