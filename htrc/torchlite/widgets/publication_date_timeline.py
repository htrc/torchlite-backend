from typing import Any, Literal

from pydantic import BaseModel, Field

from htrc.torchlite.widgets.base import WidgetBase


class PublicationDateTimelineWidget(WidgetBase, BaseModel):
    type: Literal['PublicationDateTimeline'] = 'PublicationDateTimeline'
    min_year: int | None = Field(None, alias='minYear')
    max_year: int | None = Field(None, alias='maxYear')

    def get_data(self) -> Any:
        pass
