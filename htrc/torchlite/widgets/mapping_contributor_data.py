from typing import Any, Literal

from .base import WidgetBase
from ..utils import make_list


class MappingContributorDataWidget(WidgetBase):
    type: Literal['MappingContributorData'] = 'MappingContributorData'

    def get_data(self, volumes: dict) -> Any:
        viaf_ids = list({c['id'] for v in volumes for c in make_list(v.contributor)})

        return viaf_ids
