from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base


class BaseMixin:
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.now,
        index=True
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now,
        index=True,
        onupdate=datetime.now
    )


Base = declarative_base(cls=BaseMixin)
