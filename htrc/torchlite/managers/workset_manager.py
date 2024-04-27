from typing import Annotated

from fastapi import Depends

from htrc.torchlite.config import config
from htrc.torchlite.models.workset import WorksetSummary
from htrc.torchlite.utils import load_yaml
from htrc.torchlite.http_client import http
import json


class _WorksetManager:

    def __init__(self):
        self.featured_worksets = None
        self.public_worksets = None

    async def get_featured_worksets(self) -> dict[str, WorksetSummary]:
        if self.featured_worksets is None:
            data = await load_yaml(config.FEATURED_WORKSETS_URL)
            self.featured_worksets = {
                workset['id']: WorksetSummary.model_construct(**workset)
                for workset in data['featured_worksets']
            }

        return self.featured_worksets
    
    async def get_public_workset(self) -> dict[str, WorksetSummary]:
        if self.public_worksets is None:
            headers = {'Accept': 'application/json'}
            response = await http.get(f"{config.REGISTRY_API_URL}/publicworksets", headers=headers)
            data = json.loads(response.content)
            self.public_worksets = {
                workset['metadata']['id']: WorksetSummary.model_construct(numVolumes=workset['metadata']['volumeCount'],isPublic=workset['metadata']['public'],**workset['metadata'])
                for workset in data['worksets']['workset']
            }

        return self.public_worksets

    def is_valid_workset(self, wsid: str) -> bool:
        return wsid in self.featured_worksets


WorksetManager = Annotated[_WorksetManager, Depends()]
