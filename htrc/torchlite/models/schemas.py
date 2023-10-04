from uuid import UUID

from bson import ObjectId
from pydantic import BaseModel, Field

from .mongo import PyObjectId


class WorksetSummary(BaseModel):
    id: str
    name: str
    description: str
    author: str
    is_public: bool = Field(..., alias='isPublic')
    num_volumes: int = Field(..., alias='numVolumes')

    class Config:
        allow_population_by_field_name = True


class VolumeMetadata(BaseModel):
    htid: str
    title: str
    pub_date: int | None = Field(..., alias='pubDate')
    genre: str | list[str]
    type_of_resource: str = Field(..., alias='typeOfResource')
    category: str | list[str] | None
    contributor: str | list[str] | None
    publisher: str | list[str] | None
    access_rights: str = Field(..., alias='accessRights')
    pub_place: str | list[str] | None = Field(..., alias='pubPlace')
    language: str | list[str] | None
    source_institution: str = Field(..., alias='sourceInstitution')

    class Config:
        allow_population_by_field_name = True


class WorksetInfo(WorksetSummary):
    volumes: list[VolumeMetadata]

    class Config:
        allow_population_by_field_name = True


class FilterSettings(BaseModel):
    title: list[str]
    pub_date: list[int] = Field(..., alias='pubDate')
    genre: list[str]
    type_of_resource: list[str] = Field(..., alias='typeOfResource')
    category: list[str]
    contributor: list[str]
    publisher: list[str]
    access_rights: list[str] = Field(..., alias='accessRights')
    pub_place: list[str] = Field(..., alias='pubPlace')
    language: list[str]
    source_institution: list[str] = Field(..., alias='sourceInstitution')

    class Config:
        allow_population_by_field_name = True


class Widget(BaseModel):
    type: str


class DashboardSummary(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    owner: UUID | None
    title: str | None
    description: str | None
    workset_id: str = Field(..., alias='worksetId')
    filters: FilterSettings | None
    widgets: list[Widget]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class DashboardPatch(BaseModel):
    workset_id: str | None = Field(..., alias='worksetId')
    filters: FilterSettings | None
    widgets: list[Widget] | None

    class Config:
        allow_population_by_field_name = True
