from typing import Any, Literal

from pydantic import BaseModel

from htrc.torchlite.widgets.base import WidgetBase


class MappingContributorDataWidget(WidgetBase, BaseModel):
    type: Literal['MappingContributorData'] = 'MappingContributorData'

    def get_data(self) -> Any:
        pass

