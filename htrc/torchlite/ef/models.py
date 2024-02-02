from datetime import datetime
from typing import Literal

from ..models.base import BaseModel


class Workset(BaseModel):
    id: str
    htids: list[str]
    created: datetime


class Contributor(BaseModel):
    id: str
    type: str
    name: str


class Publisher(BaseModel):
    id: str
    type: str
    name: str


class PublicationPlace(BaseModel):
    id: str
    type: str
    name: str | None = None


class SourceInstitution(BaseModel):
    type: str
    name: str


class Journal(BaseModel):
    id: str
    type: str
    journal_title: str


VolumeType = Literal["DataFeedItem", "Book", "PublicationVolume", "CreativeWork"]


class VolumeMetadata(BaseModel):
    schema_version: str | None
    id: str | None
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
    genre: str | list[str] | None = None
    type_of_resource: str | None = None
    last_rights_update_date: int | None = None
    is_part_of: Journal | None = None


class PosSectionFeatures(BaseModel):
    token_count: int | None = None
    line_count: int | None = None
    empty_line_count: int | None = None
    sentence_count: int | None = None
    cap_alpha_seq: int | None = None
    begin_char_count: dict[str, int] | None = None
    end_char_count: dict[str, int] | None = None
    token_pos_count: dict | None


class SectionFeatures(BaseModel):
    token_count: int | None = None
    line_count: int | None = None
    empty_line_count: int | None = None
    sentence_count: int | None = None
    cap_alpha_seq: int | None = None
    begin_char_count: dict[str, int] | None = None
    end_char_count: dict[str, int] | None = None
    tokens_count: dict | None


class PageFeatures(BaseModel):
    seq: str | None = None
    version: str | None = None
    token_count: int | None = None
    line_count: int | None = None
    empty_line_count: int | None = None
    sentence_count: int | None = None
    header: PosSectionFeatures | SectionFeatures | None = None
    body: PosSectionFeatures | SectionFeatures | None = None
    footer: PosSectionFeatures | SectionFeatures | None = None
    calculated_language: str | None = None


class VolumeFeatures(BaseModel):
    type: str | None = None
    id: str | None = None
    schema_version: str | None = None
    date_created: int | None = None
    page_count: int | None = None
    pages: list[PageFeatures] = []


class Volume(BaseModel):
    htid: str
    metadata: VolumeMetadata
    features: VolumeFeatures | None = None
