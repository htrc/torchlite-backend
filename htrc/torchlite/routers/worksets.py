from fastapi import APIRouter, Depends
from uuid import UUID
from typing import Annotated

from ..converters import torchlite_volume_meta_from_ef
from ..ef.api import ef_api
from ..managers.workset_manager import WorksetManager
from ..models.workset import WorksetSummary, WorksetInfo, WorksetIdMapping
from ..database import mongo_client
from ..auth.auth import get_current_user

router = APIRouter(
    prefix="/worksets",
    tags=["worksets"],
)


@router.get("/", response_model_exclude_defaults=True)
async def list_worksets(workset_manager: WorksetManager, user: Annotated[str | None, Depends(get_current_user)]) -> dict[str, list[WorksetSummary]]:
    user_id = UUID(user.get("htrc-guid", user.sub)) if user else None
    print(user_id)
    public_worksets = await workset_manager.get_public_worksets()
    featured_worksets = workset_manager.get_featured_worksets()
    user_worksets = await workset_manager.get_user_worksets()
    print(user_worksets)

    return { 'public': sorted(list(public_worksets.values()),key=lambda d: d.name), 'featured': sorted(list(featured_worksets.values()),key=lambda d: d.name), 'user': []}


@router.get("/{imported_id}/metadata", response_model_exclude_defaults=True)
async def get_workset_metadata(imported_id: str, workset_manager: WorksetManager) -> WorksetInfo:
    imported_id_mapping = await WorksetIdMapping.from_mongo(mongo_client.db["id-mappings"].find({"importedId": UUID(imported_id)}).to_list(1000))
    if len(imported_id_mapping):
        imported_id_mapping = imported_id_mapping[0]
        ef_wsid = imported_id_mapping.workset_id
    else:
        imported_volumes = await workset_manager.get_public_workset_volumes(imported_id)
        ef_wsid = await ef_api.create_workset(' '.join(imported_volumes))
        mongo_client.db["id-mappings"].insert_one({"importedId": UUID(imported_id), "worksetId": ef_wsid})

    volumes = await ef_api.get_workset_metadata(ef_wsid)
    workset = (await workset_manager.get_public_worksets())[imported_id]
    volumes_meta = [torchlite_volume_meta_from_ef(vol) for vol in volumes]
    workset_info = WorksetInfo.model_construct(**workset.model_dump(), volumes=volumes_meta)
    return workset_info
