from typing import Any, Literal

from .base import WidgetBase
from ..utils import make_list


class MappingContributorDataWidget(WidgetBase):
    type: Literal['MappingContributorData'] = 'MappingContributorData'

    @classmethod
    def get_contributor_ids(cls, volumes: dict) -> list[str]:
        contributor_ids = list({
            contributor['id']
            for v in volumes
            for contributor in make_list(v.contributor)
            if contributor['type'] == "http://id.loc.gov/ontologies/bibframe/Person"
        })

        return contributor_ids

    async def get_data(self, volumes: dict) -> Any:
        contributor_ids = self.get_contributor_ids(volumes)


        return None
