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
    pub_date: int | str | None = None
    genre: str | list[str]
    type_of_resource: str | None = None
    category: str | list[str] | None = None
    contributor: str | list[str] | None = None
    publisher: str | list[str] | None = None
    access_rights: str
    pub_place: str | list[str] | None = None
    language: str | list[str] | None = None
    source_institution: str


class WorksetInfo(WorksetSummary):
    volumes: list[VolumeMetadata]
