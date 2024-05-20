from collections import Counter
from typing import Literal

from pydantic import BaseModel

from .base import WidgetBase, WidgetDataTypes
from ..ef import models as ef_models


class PubDateEntry(BaseModel):
    year: int
    count: int


class PublicationDateTimelineWidget(WidgetBase):
    type: Literal['PublicationDateTimeline'] = 'PublicationDateTimeline'
    data_type: WidgetDataTypes = WidgetDataTypes.metadata_only

    min_year: int | None = None
    max_year: int | None = None

    async def get_data(self, volumes: list[ef_models.Volume]) -> list[PubDateEntry]:
        pub_date_counter = Counter(
            v.metadata.pub_date 
            for v in volumes if 
            v.metadata.pub_date is not None and (isinstance(v.metadata.pub_date, int) or v.metadata.pub_date.isdigit()))
        return sorted([
            PubDateEntry.model_construct(year=int(year), count=count)
            for year, count in pub_date_counter.items()
        ], key=lambda d: d.year)
