from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, RelationshipProperty

from typing import List
from .database import Base


class Dashboard(Base):
    __tablename__ = "dashboards"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)
    workset = Column(String)

    widgets: RelationshipProperty[List["Widget"]] = relationship("Widget", back_populates="dashboard")


class Widget(Base):
    __tablename__ = "widgets"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)
    widget_type = Column(String)
    dashboard_id = Column(Integer, ForeignKey("dashboards.id"))

    dashboard: RelationshipProperty[Dashboard] = relationship("Dashboard", back_populates="widgets")
