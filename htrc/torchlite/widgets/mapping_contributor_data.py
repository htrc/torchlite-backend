from typing import Any, Literal

from .base import WidgetBase
from ..models.workset import WorksetInfo


class MappingContributorDataWidget(WidgetBase):
    type: Literal['MappingContributorData'] = 'MappingContributorData'

    def get_data(self, workset_info: WorksetInfo) -> Any:
        return workset_info.model_dump()
