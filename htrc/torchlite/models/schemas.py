from pydantic import BaseModel


class WorksetSummary(BaseModel):
    id: str
    name: str
    description: str
    author: str
    isPublic: bool
    numVolumes: int


class VolumeMetadata(BaseModel):
    htid: str
    title: str
    pubDate: int | None
    genre: str | list[str]
    typeOfResource: str
    category: str | list[str] | None
    contributor: str | list[str] | None
    publisher: str | list[str] | None
    accessRights: str
    pubPlace: str | list[str] | None
    language: str | list[str] | None
    sourceInstitution: str


class WorksetInfo(WorksetSummary):
    volumes: list[VolumeMetadata]


class FilterSettings(BaseModel):
    title: list[str]
    pubDate: list[int]
    genre: list[str]
    typeOfResource: list[str]
    category: list[str]
    contributor: list[str]
    publisher: list[str]
    accessRights: list[str]
    pubPlace: list[str]
    language: list[str]
    sourceInstitution: list[str]


class Widget(BaseModel):
    type: str


class DashboardSummary(BaseModel):
    id: str
    owner: str
    title: str
    description: str
    worksetId: str
    filters: FilterSettings
    widgets: list[Widget]


class DashboardPatch(BaseModel):
    workset_id: str | None
    filters: FilterSettings | None
    widgets: list[Widget] | None
