from .converters import torchlite_volume_meta_from_ef
from .ef.models import Volume
from .models.dashboard import FilterSettings
from .utils import make_set


def apply_filters(volumes: list[Volume], filters: FilterSettings) -> list[Volume]:
    filtered_volumes = []
    for volume in volumes:
        volume_meta = torchlite_volume_meta_from_ef(volume)
        if filters.titles and volume_meta.title not in filters.titles:
            continue
        if filters.pub_dates and volume_meta.pub_date not in filters.pub_dates:
            continue
        if filters.genres and not make_set(volume_meta.genre).intersection(filters.genres):
            continue
        if filters.type_of_resources and volume_meta.type_of_resource not in filters.type_of_resources:
            continue
        if filters.categories and not make_set(volume_meta.category).intersection(filters.categories):
            continue
        if filters.contributors and not make_set(volume_meta.contributor).intersection(filters.contributors):
            continue
        if filters.publishers and not make_set(volume_meta.publisher).intersection(filters.publishers):
            continue
        if filters.access_rights and volume_meta.access_rights not in filters.access_rights:
            continue
        if filters.pub_places and not make_set(volume_meta.pub_place).intersection(filters.pub_places):
            continue
        if filters.languages and not make_set(volume_meta.language).intersection(filters.languages):
            continue
        if filters.source_institutions and volume_meta.source_institution not in filters.source_institutions:
            continue

        filtered_volumes.append(volume)

    return filtered_volumes
