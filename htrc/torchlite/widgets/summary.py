from collections import Counter
from typing import Literal

from pydantic import BaseModel

from .base import WidgetBase, WidgetDataTypes
from ..ef import models as ef_models


class SummaryWidget(WidgetBase):
    type: Literal['Summary'] = 'Summary'
    data_type: WidgetDataTypes = WidgetDataTypes.vols_with_pos

    async def get_data(self, volumes: list[ef_models.Volume]) -> dict:
        return {}
