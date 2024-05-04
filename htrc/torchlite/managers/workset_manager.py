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

    def get_featured_worksets(self) -> dict[str, WorksetSummary]:
        if self.featured_worksets is None:
            self.featured_worksets = {
                workset: self.public_worksets[workset]
                for workset in self.public_worksets if self.public_worksets[workset].author == config.FEATURED_WORKSET_USER
            }

        return self.featured_worksets

    async def get_public_worksets(self) -> dict[str, WorksetSummary]:
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
        if type(wsid) != str:
            wsid_string = str(wsid)
        else:
            wsid_string = wsid

        return wsid_string in self.public_worksets


WorksetManager = Annotated[_WorksetManager, Depends()]
