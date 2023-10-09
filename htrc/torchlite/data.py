import json

from .converters import torchlite_volume_meta_from_ef
from .ef.models import Volume
from .models.dashboard import FilterSettings
from .models.workset import WorksetSummary
from .utils import make_set

with open('data/worksets.json', 'r') as f:
    arr = json.load(f)
    worksets: dict[str, WorksetSummary] = {w['id']: WorksetSummary(**w) for w in arr}


def apply_filters(volumes: list[Volume], filters: FilterSettings) -> list[Volume]:
    filtered_volumes = []
    for volume in volumes:
        volume_meta = torchlite_volume_meta_from_ef(volume)
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
