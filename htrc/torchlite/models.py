from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Dashboard(Base):
    __tablename__ = "dashboards"

    id = Column(Integer, primary_key=True, index=True)
    workset = Column(Integer)

    widgets = relationship("Widget", back_populates="dashboard")


class Widget(Base):
    __tablename__ = "widgets"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    dashboard_id = Column(Integer, ForeignKey("dashboards.id"))

    dashboard = relationship("Dashboard", back_populates="widgets")
