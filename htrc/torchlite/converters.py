from .ef.api import models as ef_models
from .models.workset import VolumeMetadata
from .utils import parse_value


def torchlite_volume_meta_from_ef(ef_vol: ef_models.Volume) -> VolumeMetadata:
    return VolumeMetadata(
        htid=ef_vol.htid,
        title=ef_vol.metadata.title,
        pub_date=ef_vol.metadata.pub_date,
        genre=ef_vol.metadata.genre,
        type_of_resource=ef_vol.metadata.type_of_resource,
        category=ef_vol.metadata.category,
        contributor=parse_value(ef_vol.metadata.contributor, "name"),
        publisher=parse_value(ef_vol.metadata.publisher, "name"),
        access_rights=ef_vol.metadata.access_rights,
        pub_place=parse_value(ef_vol.metadata.pub_place, "name"),
        language=ef_vol.metadata.language,
        source_institution=parse_value(ef_vol.metadata.source_institution, "name"),
    )
