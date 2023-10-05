from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, conlist

from .mongo import PyUuid, MongoModel


class WorksetSummary(BaseModel):
    id: str
    name: str
    description: str
    author: str
    is_public: bool = Field(..., alias="isPublic")
    num_volumes: int = Field(..., alias="numVolumes")

    class Config:
        allow_population_by_field_name = True


class VolumeMetadata(BaseModel):
    htid: str
    title: str
    pub_date: int | None = Field(..., alias="pubDate")
    genre: str | list[str]
    type_of_resource: str = Field(..., alias="typeOfResource")
    category: str | list[str] | None
    contributor: str | list[str] | None
    publisher: str | list[str] | None
    access_rights: str = Field(..., alias="accessRights")
    pub_place: str | list[str] | None = Field(..., alias="pubPlace")
    language: str | list[str] | None
    source_institution: str = Field(..., alias="sourceInstitution")

    class Config:
        allow_population_by_field_name = True


class WorksetInfo(WorksetSummary):
    volumes: list[VolumeMetadata]

    class Config:
        allow_population_by_field_name = True


class FilterSettings(BaseModel):
    title: list[str] = []
    pub_date: list[int] = Field([], alias="pubDate")
    genre: list[str] = []
    type_of_resource: list[str] = Field([], alias="typeOfResource")
    category: list[str] = []
    contributor: list[str] = []
    publisher: list[str] = []
    access_rights: list[str] = Field([], alias="accessRights")
    pub_place: list[str] = Field([], alias="pubPlace")
    language: list[str] = []
    source_institution: list[str] = Field([], alias="sourceInstitution")

    class Config:
        allow_population_by_field_name = True


class Widget(BaseModel):
    type: Literal['MappingContributorData', 'PublicationDateTimeline']


class Dashboard(BaseModel):
    id: PyUuid = Field(default_factory=PyUuid)
    workset_id: str = Field(..., alias="worksetId")
    filters: FilterSettings | None
    widgets: list[Widget]


class DashboardSummary(Dashboard, MongoModel):
    owner: UUID | None
    title: str | None
    description: str | None
    is_shared: bool = Field(False, alias="isShared")
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt")


class DashboardCreate(MongoModel):
    title: str | None = None
    description: str | None = None
    workset_id: str = Field(..., alias="worksetId")
    filters: FilterSettings | None = None
    widgets: conlist(Widget, min_items=1, unique_items=True)


class DashboardPatch(MongoModel):
    workset_id: str | None = Field(None, alias="worksetId")
    filters: FilterSettings | None = None
    widgets: list[Widget] | None = None
    is_shared: bool | None = Field(None, alias="isShared")


class DashboardPatchUpdate(DashboardPatch):
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt")
