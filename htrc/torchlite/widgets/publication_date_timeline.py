from collections import Counter
from typing import Literal

from pydantic import BaseModel

from .base import WidgetBase
from ..ef import models as ef_models


class PubDateEntry(BaseModel):
    year: int
    count: int


class PublicationDateTimelineWidget(WidgetBase):
    type: Literal['PublicationDateTimeline'] = 'PublicationDateTimeline'
    min_year: int | None = None
    max_year: int | None = None

    async def get_data(self, volumes: list[ef_models.Volume]) -> list[PubDateEntry]:
        pub_date_counter = Counter(v.metadata.pub_date for v in volumes if v.metadata.pub_date is not None)
        return sorted([
            PubDateEntry.model_construct(year=int(year), count=count)
            for year, count in pub_date_counter.items()
        ], key=lambda d: d.year)
