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
    genre: str | list[str]
    type_of_resource: str
    category: str | list[str] | None
    contributor: str | list[str] | None
    publisher: str | list[str] | None
    access_rights: str
    pub_place: str | list[str] | None
    language: str | list[str] | None
    source_institution: str


class WorksetInfo(WorksetSummary):
    volumes: list[VolumeMetadata]
