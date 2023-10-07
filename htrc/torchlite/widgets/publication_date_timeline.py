from collections import Counter
from typing import Any, Literal

from .base import WidgetBase


class PublicationDateTimelineWidget(WidgetBase):
    type: Literal['PublicationDateTimeline'] = 'PublicationDateTimeline'
    min_year: int | None = None
    max_year: int | None = None

    def get_data(self, volumes: dict) -> Any:
        pub_date_counter = Counter(v['metadata']['pubDate'] for v in volumes if v['metadata']['pubDate'] is not None)
        return sorted([
            {'year': int(year), 'count': count}
            for year, count in pub_date_counter.items()
        ], key=lambda d: d['year'])
