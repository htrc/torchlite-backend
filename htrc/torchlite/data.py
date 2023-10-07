import json

from .models.dashboard import FilterSettings
from .models.workset import WorksetSummary, VolumeMetadata, WorksetInfo
from .utils import make_set, parse_value

with open('data/worksets.json', 'r') as f:
    arr = json.load(f)
    worksets: dict[str, WorksetSummary] = {w['id']: WorksetSummary(**w) for w in arr}


def sanitize(data):
    if isinstance(data, str):
        return data.strip() or None
    elif isinstance(data, dict):
        return {k: sanitize(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [v for e in data if (v := sanitize(e)) is not None] or None
    else:
        return data


def parse_volume_meta(vol: dict) -> VolumeMetadata:
    meta = vol['metadata']
    return VolumeMetadata(
        htid=vol['htid'],
        title=meta['title'],
        pub_date=meta.get('pubDate'),
        genre=meta['genre'],
        type_of_resource=meta['typeOfResource'],
        category=meta.get('category'),
        contributor=parse_value(meta.get('contributor')),
        publisher=parse_value(meta.get('publisher')),
        access_rights=meta['accessRights'],
        pub_place=parse_value(meta.get('pubPlace')),
        language=meta.get('language'),
        source_institution=parse_value(meta['sourceInstitution']),
    )


def get_workset_info(workset_id: str) -> WorksetInfo:
    with open(f'data/{workset_id}.json', 'r') as f:
        data = sanitize(json.load(f))

    volumes = [parse_volume_meta(vol) for vol in data['data']]
    ws = worksets[workset_id]

    return WorksetInfo.model_construct(**ws.model_dump(), volumes=volumes)


def get_full_meta(workset_id: str) -> dict:
    with open(f'data/{workset_id}.json', 'r') as f:
        data = sanitize(json.load(f))

    return data['data']


def apply_filters(volumes: list[dict], filters: FilterSettings) -> list[dict]:
    filtered_volumes = []
    for volume in volumes:
        volume_meta = parse_volume_meta(volume)
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

        filtered_volumes.append(volume)

    return filtered_volumes
