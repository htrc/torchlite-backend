import uuid
from datetime import datetime
from uuid import UUID

from pydantic import Field, conlist

from .base import BaseModel
from .mongo import PyUuid, MongoModel
from ..widgets import ALL_WIDGETS


class FilterSettings(BaseModel):
    title: list[str] = []
    pub_date: list[int] = []
    genre: list[str] = []
    type_of_resource: list[str] = []
    category: list[str] = []
    contributor: list[str] = []
    publisher: list[str] = []
    access_rights: list[str] = []
    pub_place: list[str] = []
    language: list[str] = []
    source_institution: list[str] = []


class Dashboard(BaseModel, arbitrary_types_allowed=True):
    id: PyUuid = Field(default_factory=uuid.uuid4)
    workset_id: str
    filters: FilterSettings | None
    widgets: list[ALL_WIDGETS]


class DashboardSummary(Dashboard, MongoModel):
    owner: UUID | None
    title: str | None = None
    description: str | None = None
    is_shared: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class DashboardCreate(MongoModel):
    title: str | None = None
    description: str | None = None
    workset_id: str
    filters: FilterSettings | None = None
    widgets: conlist(ALL_WIDGETS, min_length=1)


class DashboardPatch(MongoModel):
    workset_id: str | None = None
    filters: FilterSettings | None = None
    widgets: list[ALL_WIDGETS] | None = None
    is_shared: bool | None = None


class DashboardPatchUpdate(DashboardPatch):
    updated_at: datetime = Field(default_factory=datetime.now)
