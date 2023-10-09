from pydantic import AnyUrl, AnyHttpUrl

from .base import BaseModel


class WorksetSummary(BaseModel):
    id: str
    name: str
    description: str
    author: str
    is_public: bool
    num_volumes: int


class VolumeMetadata(BaseModel):
    htid: str
    title: str
    pub_date: int | None
    genre: AnyUrl | list[AnyUrl]
    type_of_resource: AnyHttpUrl
    category: str | list[str] | None
    contributor: str | list[str] | None
    publisher: str | list[str] | None
    access_rights: str
    pub_place: str | list[str] | None
    language: str | list[str] | None
    source_institution: str


class WorksetInfo(WorksetSummary):
    volumes: list[VolumeMetadata]
