import uuid
from datetime import datetime
from uuid import UUID

from pydantic import Field, conlist

from .base import BaseModel
from .mongo import PyUuid, MongoModel
from ..widgets import ALL_WIDGETS


class FilterSettings(BaseModel):
    titles: list[str] = []
    pub_dates: list[int] = []
    genres: list[str] = []
    type_of_resources: list[str] = []
    categories: list[str] = []
    contributors: list[str] = []
    publishers: list[str] = []
    access_rights: list[str] = []
    pub_places: list[str] = []
    languages: list[str] = []
    source_institutions: list[str] = []

class DataCleaningSettings(BaseModel):
    language: str | None = None

class Dashboard(BaseModel, arbitrary_types_allowed=True):
    id: PyUuid = Field(default_factory=uuid.uuid4)
    imported_id: UUID
#    workset_id: str
    filters: FilterSettings | None
    datacleaning: DataCleaningSettings | None
    widgets: list[ALL_WIDGETS]


class DashboardSummary(Dashboard, MongoModel):
    owner: UUID | None
    title: str | None = None
    description: str | None = None
    is_shared: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    imported_id: UUID | None = None


class DashboardCreate(MongoModel):
    title: str | None = None
    description: str | None = None
#    workset_id: str
    imported_id: UUID
    filters: FilterSettings | None = None
    widgets: conlist(ALL_WIDGETS, min_length=1)


class DashboardPatch(MongoModel):
#    workset_id: str | None = None
    imported_id: UUID | None = None
    filters: FilterSettings | None = None
    widgets: list[ALL_WIDGETS] | None = None
    is_shared: bool | None = None


class DashboardPatchUpdate(DashboardPatch):
    updated_at: datetime = Field(default_factory=datetime.now)
