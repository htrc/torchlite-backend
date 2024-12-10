from typing import Annotated

from fastapi import Depends
from authlib.oidc.core import UserInfo
from htrc.torchlite.config import config
from htrc.torchlite.models.workset import WorksetSummary
from htrc.torchlite.http_client import registry_http
import json


class _WorksetManager:

    def __init__(self):
        self.featured_worksets = None
        self.public_worksets = None
        self.user_worksets = None

    def get_featured_worksets(self) -> dict[str, WorksetSummary]:
        if self.featured_worksets is None:
            print("FEATURED WORKSET USER")
            print(config.FEATURED_WORKSET_USER)
            self.featured_worksets = {
                workset: self.public_worksets[workset]
                for workset in self.public_worksets if self.public_worksets[workset].author == config.FEATURED_WORKSET_USER
            }
        print("public worksets")
        for ws in self.public_worksets:
            print(self.public_worksets[ws])
            print(self.public_worksets[ws].author)

        return self.featured_worksets

    async def get_public_worksets(self) -> dict[str, WorksetSummary]:
        if self.public_worksets is None:
            headers = {'Accept': 'application/json'}
            response = await registry_http.get(f"{config.REGISTRY_API_URL}/publicworksets", headers=headers)
            data = json.loads(response.content)
            self.public_worksets = {
                workset['metadata']['id']: WorksetSummary.model_construct(numVolumes=workset['metadata']['volumeCount'],isPublic=workset['metadata']['public'],**workset['metadata'])
                for workset in data['worksets']['workset'] if workset['metadata']['public']
            }

        return self.public_worksets

    async def get_user_worksets(self, user_access_token: str | None) -> dict[str, WorksetSummary]:
        if self.user_worksets is None and user_access_token is not None:
            headers = {'Accept': 'application/json', 'Authorization': user_access_token}
            response = await registry_http.get(f"{config.REGISTRY_API_URL}/worksets", headers=headers)
            try:
                data = json.loads(response.content)

                self.user_worksets = {
                    workset['metadata']['id']: WorksetSummary.model_construct(numVolumes=workset['metadata']['volumeCount'],isPublic=workset['metadata']['public'],**workset['metadata'])
                    for workset in data['worksets']['workset']
                }
            except Exception as e:
                print(f'ERROR getting user worksets: {e}')

        return self.user_worksets
    
    async def get_public_workset_volumes(self, wsid: str) -> str:
        headers = {'Accept': 'application/json'}
        response = await registry_http.get(f"{config.REGISTRY_API_URL}/publicworksets/{wsid}", headers=headers)
        data = json.loads(response.content)
        return [htid['id'] for htid in data['workset']['content']['volumes']['volume']]
    
    async def get_user_workset_volumes(self, wsid: str, user_access_token: UserInfo) -> str:
        headers = {'Accept': 'application/json', 'Authorization': user_access_token}
        response = await registry_http.get(f"{config.REGISTRY_API_URL}/worksets/{wsid}", headers=headers)
        data = json.loads(response.content)
        return [htid['id'] for htid in data['workset']['content']['volumes']['volume']]

    def is_valid_workset(self, wsid: str) -> bool:
        if isinstance(wsid,str):
            wsid_string = wsid
        else:
            wsid_string = str(wsid)

        try:
            if wsid_string in self.public_worksets or wsid_string in self.user_worksets:
                return True
            else:
                return False
        except TypeError:
            return False


WorksetManager = Annotated[_WorksetManager, Depends()]
