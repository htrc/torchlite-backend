from enum import Enum
from pydantic import BaseModel


class FacetsEnum(str, Enum):
    publication_title = "publication_title"
    publication_date = "publication_date"
    genre = "genre"
    resource_type = "resource_type"
    category = "category"
    contributor = "contributor"
    publisher = "publisher"
    access_rights = "access_rights"
    place_of_publication = "place_of_publication"


class WidgetBase(BaseModel):
    pass


class WidgetCreate(WidgetBase):
    pass


class Widget(WidgetBase):
    id: int
    dashboard_id: int
    widget_type: str

    class Config:
        orm_mode = True


class DashboardBase(BaseModel):
    pass


class DashboardCreate(DashboardBase):
    pass


class Dashboard(DashboardBase):
    id: int
    workset: str | None = None
    widgets: list[Widget] = []

    class Config:
        orm_mode = True
