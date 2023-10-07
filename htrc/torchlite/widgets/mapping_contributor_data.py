from typing import Any, Literal

from .base import WidgetBase


class MappingContributorDataWidget(WidgetBase):
    type: Literal['MappingContributorData'] = 'MappingContributorData'

    def get_data(self) -> Any:
        pass
