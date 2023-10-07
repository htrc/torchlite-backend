from typing import Any, Literal

from .base import WidgetBase
from ..models.workset import WorksetInfo


class PublicationDateTimelineWidget(WidgetBase):
    type: Literal['PublicationDateTimeline'] = 'PublicationDateTimeline'
    min_year: int | None = None
    max_year: int | None = None

    def get_data(self, workset_info: WorksetInfo) -> Any:
        return workset_info.model_dump()
