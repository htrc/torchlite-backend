from typing import Annotated

from fastapi import Depends

from htrc.torchlite.config import config
from htrc.torchlite.models.workset import WorksetSummary
from htrc.torchlite.utils import load_yaml


class _WorksetManager:

    def __init__(self):
        self.featured_worksets = None

    async def get_featured_worksets(self) -> dict[str, WorksetSummary]:
        if self.featured_worksets is None:
            data = await load_yaml(config.FEATURED_WORKSETS_URL)
            self.featured_worksets = {
                workset['id']: WorksetSummary.model_construct(**workset)
                for workset in data['featured_worksets']
            }

        return self.featured_worksets

    def is_valid_workset(self, wsid: str) -> bool:
        return wsid in self.featured_worksets


WorksetManager = Annotated[_WorksetManager, Depends()]
