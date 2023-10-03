import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

from htrc.torchlite.database import Base


class Dashboard(Base):
    __tablename__ = 'dashboards'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    owner_id = Column(UUID(as_uuid=True), index=True)
    title = Column(String)
    description = Column(String)
    workset_id = Column(String, index=True, nullable=False)
    filters = Column(JSONB, default=dict)
    widgets = Column(ARRAY(String))
