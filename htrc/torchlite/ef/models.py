from typing import Literal

from pydantic import AnyHttpUrl, AnyUrl

from ..models.base import BaseModel


class Workset(BaseModel):
    id: str
    htids: list[str]
    created: int


class Contributor(BaseModel):
    id: AnyHttpUrl
    type: AnyHttpUrl
    name: str


class Publisher(BaseModel):
    id: AnyHttpUrl
    type: AnyHttpUrl
    name: str


class PublicationPlace(BaseModel):
    id: AnyHttpUrl
    type: AnyHttpUrl
    name: str | None = None


class SourceInstitution(BaseModel):
    type: AnyHttpUrl
    name: str


class Journal(BaseModel):
    id: AnyHttpUrl
    type: str
    journalTitle: str


VolumeType = Literal["DataFeedItem", "Book", "PublicationVolume", "CreativeWork"]


class VolumeMetadata(BaseModel):
    schema_version: AnyHttpUrl | None
    id: AnyHttpUrl | None
    type: VolumeType | list[VolumeType]
    date_created: int
    title: str | None  # only for "Book" or "CreativeWork"
    alternate_title: str | list[str] | None = None
    enumeration_chronology: str | None = None
    contributor: Contributor | list[Contributor] | None = None
    pub_date: int | None
    publisher: Publisher | list[Publisher] | None = None
    pub_place: PublicationPlace | list[PublicationPlace] | None = None
    language: str | list[str] | None = None
    access_rights: Literal[
        "pd", "ic", "op", "orph", "und", "ic-world", "nobody", "pdus", "cc-by-3.0", "cc-by-nd-3.0", "cc-by-nc-nd-3.0",
        "cc-by-nc-3.0", "cc-by-nc-sa-3.0", "cc-by-sa-3.0", "orphcand", "cc-zero", "und-world", "icus", "cc-by-4.0",
        "cc-by-nd-4.0", "cc-by-nc-nd-4.0", "cc-by-nc-4.0", "cc-by-nc-sa-4.0", "cc-by-sa-4.0", "pd-pvt", "supp"
    ]
    access_profile: Literal["open", "google", "page", "page+lowres"]
    source_institution: SourceInstitution
    main_entity_of_page: list[str] | None = None
    lcc: str | list[str] | None = None
    oclc: str | list[str] | None = None
    issn: str | list[str] | None = None
    isbn: str | list[str] | None = None
    category: str | list[str] | None = None
    genre: AnyUrl | list[AnyUrl] | None = None
    type_of_resource: AnyHttpUrl | None = None
    last_rights_update_date: int | None = None
    is_part_of: Journal | None = None


class Volume(BaseModel):
    htid: str
    metadata: VolumeMetadata
    # features: VolumeFeatures
