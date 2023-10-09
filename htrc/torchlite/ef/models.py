from typing import Literal

from pydantic import AnyHttpUrl

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
    name: str


class SourceInstitution(BaseModel):
    type: AnyHttpUrl
    name: str


class Journal(BaseModel):
    id: AnyHttpUrl
    type: str
    journalTitle: str


class VolumeMetadata(BaseModel):
    schema_version: AnyHttpUrl | None
    id: AnyHttpUrl | None
    type: Literal["DataFeedItem", "Book", "PublicationVolume", "CreativeWork"]
    date_created: int
    title: str | None  # only for "Book" or "CreativeWork"
    alternate_title: str | list[str] | None
    enumeration_chronology: str | None
    contributor: Contributor | list[Contributor] | None
    pub_date: int | None
    publisher: Publisher | list[Publisher] | None
    pub_place: PublicationPlace | list[PublicationPlace] | None
    language: str | list[str] | None
    access_rights: Literal[
        "pd", "ic", "op", "orph", "und", "ic-world", "nobody", "pdus", "cc-by-3.0", "cc-by-nd-3.0", "cc-by-nc-nd-3.0",
        "cc-by-nc-3.0", "cc-by-nc-sa-3.0", "cc-by-sa-3.0", "orphcand", "cc-zero", "und-world", "icus", "cc-by-4.0",
        "cc-by-nd-4.0", "cc-by-nc-nd-4.0", "cc-by-nc-4.0", "cc-by-nc-sa-4.0", "cc-by-sa-4.0", "pd-pvt", "supp"
    ]
    access_profile: Literal["open", "google", "page", "page+lowres"]
    source_institution: SourceInstitution | None
    main_entity_of_page: list[str] | None
    lcc: str | list[str] | None
    oclc: str | list[str] | None
    issn: str | list[str] | None
    isbn: str | list[str] | None
    category: str | list[str] | None
    genre: AnyHttpUrl | list[AnyHttpUrl] | None
    type_of_resource: AnyHttpUrl | None
    last_rights_update_date: int | None
    is_part_of: Journal | None
