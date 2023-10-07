from typing import Any, Literal

from .base import WidgetBase


class PublicationDateTimelineWidget(WidgetBase):
    type: Literal['PublicationDateTimeline'] = 'PublicationDateTimeline'
    min_year: int | None = None
    max_year: int | None = None

    def get_data(self) -> Any:
        pass
