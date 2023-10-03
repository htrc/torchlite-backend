import json

from htrc.torchlite.models.schemas import WorksetSummary, VolumeMetadata, WorksetInfo

with open('data/worksets.json', 'r') as f:
    arr = json.load(f)
    worksets = {w['id']: WorksetSummary(**w) for w in arr}


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
    # print(meta)
    return VolumeMetadata(
        htid=sanitize(vol['htid']),
        title=sanitize(meta['title']),
        pubDate=sanitize(meta.get('pubDate')),
        genre=sanitize(meta['genre']),
        typeOfResource=sanitize(meta['typeOfResource']),
        category=sanitize(meta.get('category')),
        contributor=parse_value(meta.get('contributor')),
        publisher=parse_value(meta.get('publisher')),
        accessRights=sanitize(meta['accessRights']),
        pubPlace=parse_value(meta.get('pubPlace')),
        language=sanitize(meta.get('language')),
        sourceInstitution=parse_value(meta['sourceInstitution']),
    )


def get_workset_info(workset_id: str) -> WorksetInfo:
    with open(f'data/{workset_id}.json', 'r') as f:
        data = json.load(f)

    volumes = [parse_volume_meta(vol) for vol in data['data']]
    ws = worksets[workset_id]

    return WorksetInfo(**ws.dict(), volumes=volumes)
