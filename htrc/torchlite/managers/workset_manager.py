from typing import Annotated

from fastapi import Depends
from uuid import UUID
from authlib.oidc.core import UserInfo
from htrc.torchlite.config import config
from htrc.torchlite.models.workset import WorksetSummary
from htrc.torchlite.models.dashboard import DashboardSummary, DashboardPatch, DashboardPatchUpdate, DashboardCreate, FilterSettings
from htrc.torchlite.widgets.mapping_contributor_data import MappingContributorDataWidget
from htrc.torchlite.widgets.publication_date_timeline import PublicationDateTimelineWidget
from htrc.torchlite.widgets.simple_tag_cloud import SimpleTagCloudWidget
from htrc.torchlite.widgets.summary import SummaryWidget
from htrc.torchlite.http_client import registry_http
from ..database import mongo_client
from pymongo import ReturnDocument
import json

import logging

log = logging.getLogger(config.PROJECT_NAME)

class _WorksetManager:

    def __init__(self):
        self.featured_worksets = None
        self.public_worksets = None
        self.user_worksets = None

    def get_featured_worksets(self) -> dict[str, WorksetSummary]:
        if self.featured_worksets is None:
            self.featured_worksets = {
                workset: self.public_worksets[workset]
                for workset in self.public_worksets if self.public_worksets[workset].author == config.FEATURED_WORKSET_USER
            }

        return self.featured_worksets

    async def get_public_worksets(self) -> dict[str, WorksetSummary]:
        if self.public_worksets is None:
            try:
                headers = {'Accept': 'application/json'}
                response = await registry_http.get(f"{config.REGISTRY_API_URL}/publicworksets", headers=headers)
                data = json.loads(response.content)
                self.public_worksets = {
                    workset['metadata']['id']: WorksetSummary.model_construct(numVolumes=workset['metadata']['volumeCount'],isPublic=workset['metadata']['public'],**workset['metadata'])
                    for workset in data['worksets']['workset'] if workset['metadata']['public']
                }
            except Exception as e:
                log.error(f'ERROR getting public worksets: {e}')

        return self.public_worksets

    async def get_user_worksets(self, user_access_token: str | None) -> dict[str, WorksetSummary]:
        if self.user_worksets is None and user_access_token is not None:
            headers = {'Accept': 'application/json', 'Authorization': user_access_token}
            try:
                response = await registry_http.get(f"{config.REGISTRY_API_URL}/worksets", headers=headers)
                data = json.loads(response.content)

                self.user_worksets = {
                    workset['metadata']['id']: WorksetSummary.model_construct(numVolumes=workset['metadata']['volumeCount'],isPublic=workset['metadata']['public'],**workset['metadata'])
                    for workset in data['worksets']['workset']
                }
            except Exception as e:
                log.error(f'ERROR getting user worksets: {e}')

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

        if wsid_string in self.public_worksets:
            return True
        elif self.user_worksets and wsid_string in self.user_worksets:
            return True
        else:
            return False
        
    # Handle changes in featured worksets. Ensure all featured worksets each has their own shared
    # dashboard that can be cloned. If a workset is in the database but not listed in
    # featured_worksets, make that dashboard private. If a workset is in featured_worksets but not
    # the database, check for a private dashboard and make it public if it exists, otherwise make
    # a new dashboard for the workset 
    async def align_featured_worksets(self, shared_worksets: list[DashboardSummary]) -> list[DashboardSummary]:
        found_worksets = []
        stop_sharing = []
        for ws in shared_worksets:
            if str(ws.imported_id) in self.featured_worksets:
                found_worksets.append(str(ws.imported_id))
            else:
                stop_sharing.append(ws.imported_id)

        updated_sharing = [ w for w in shared_worksets if w.imported_id not in stop_sharing ]

        for workset in stop_sharing:
            dashboard_patch = DashboardPatch(imported_id=workset, is_shared=False)
            dashboard_patch_update = DashboardPatchUpdate(**dashboard_patch.model_dump(exclude_defaults=True))
            try:
                await DashboardSummary.from_mongo(
                    mongo_client.db["dashboards"].find_one_and_update(
                        filter={"importedId": workset, "owner": config.TORCHLITE_UID},
                        update={"$set": dashboard_patch_update.to_mongo(exclude_unset=False)},
                        return_document=ReturnDocument.AFTER
                    )
                )
            except Exception as e:
                log.error(f"ERROR turning off sharing of featured dashboard: {e}")

        new_worksets = { x: self.featured_worksets[x] for x in self.featured_worksets if x not in found_worksets }
        if len(new_worksets) > 0:
            hiden_worksets = await DashboardSummary.from_mongo(
                mongo_client.db["dashboards"].find({"owner": config.TORCHLITE_UID, "isShared": False}).to_list(1000)
            )
            for hidden_workset in hiden_worksets:
                if str(hidden_workset.imported_id) in new_worksets:
                    patch_shared_on = DashboardPatch(imported_id=hidden_workset.imported_id, is_shared=True)
                    patch_shared_on_update = DashboardPatchUpdate(**patch_shared_on.model_dump(exclude_defaults=True))

                    del new_worksets[str(hidden_workset.imported_id)]
                    try:
                        await DashboardSummary.from_mongo(
                            mongo_client.db["dashboards"].find_one_and_update(
                                filter={"importedId": hidden_workset.imported_id, "owner": config.TORCHLITE_UID},
                                update={"$set": patch_shared_on_update.to_mongo(exclude_unset=False)},
                                return_document=ReturnDocument.AFTER
                            )
                        )
                        updated_sharing.append(hidden_workset)
                    except Exception as e:
                        log.error(f"ERROR turning on sharing of featured dashboard: {e}")

        for new_workset in new_worksets:
            new_dashboard = DashboardCreate(
                title=new_worksets[new_workset].name,
                imported_id=UUID(new_workset),
                widgets=[MappingContributorDataWidget(), PublicationDateTimelineWidget(), SimpleTagCloudWidget(), SummaryWidget()],
                filters=FilterSettings())
            new_dashboard_summary = DashboardSummary(**(new_dashboard.model_dump(exclude_defaults=False)), owner=config.TORCHLITE_UID, is_shared=True)

            try:
                await mongo_client.db["dashboards"].insert_one(new_dashboard_summary.to_mongo(exclude_unset=False))
                updated_sharing.append(new_dashboard_summary)
            except Exception as e:
                log.error(f"ERROR creating new featured dashboard: {e}")

        return updated_sharing


WorksetManager = Annotated[_WorksetManager, Depends()]
