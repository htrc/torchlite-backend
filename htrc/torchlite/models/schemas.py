from uuid import UUID

from bson import ObjectId
from pydantic import BaseModel, Field

from .mongo import PyObjectId


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
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    owner_id: UUID
    title: str
    description: str
    worksetId: str
    filters: FilterSettings
    widgets: list[Widget]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        # schema_extra = {
        #     "example": {
        #     }
        # }


class DashboardPatch(BaseModel):
    workset_id: str | None
    filters: FilterSettings | None
    widgets: list[Widget] | None
