from collections import Counter
from typing import Any, Literal

from pydantic import BaseModel

from .base import WidgetBase


class PubDateEntry(BaseModel):
    year: int
    count: int


class PublicationDateTimelineWidget(WidgetBase):
    type: Literal['PublicationDateTimeline'] = 'PublicationDateTimeline'
    min_year: int | None = None
    max_year: int | None = None

    async def get_data(self, volumes: dict) -> Any:
        pub_date_counter = Counter(v['metadata']['pubDate'] for v in volumes if v['metadata']['pubDate'] is not None)
        return sorted([
            PubDateEntry.model_construct(year=int(year), count=count)
            for year, count in pub_date_counter.items()
        ], key=lambda d: d.year)
