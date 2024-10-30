from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_cache.decorator import cache
from uuid import UUID
from typing import Annotated

from ..converters import torchlite_volume_meta_from_ef
from ..ef.api import ef_api
from ..managers.workset_manager import WorksetManager
from ..models.workset import WorksetSummary, WorksetInfo, WorksetIdMapping
from ..database import mongo_client
from ..auth.auth import get_user_access_token

router = APIRouter(
    prefix="/worksets",
    tags=["worksets"],
)


@router.get("/", response_model_exclude_defaults=True)
async def list_worksets(workset_manager: WorksetManager, user_access_token: Annotated[str | None, Depends(get_user_access_token)]) -> dict[str, list[WorksetSummary]]:
    public_worksets = await workset_manager.get_public_worksets()
    featured_worksets = workset_manager.get_featured_worksets()
    user_worksets = await workset_manager.get_user_worksets(user_access_token)

    return {'public': sorted(list(public_worksets.values()), key=lambda d: d.name),
            'featured': sorted(list(featured_worksets.values()), key=lambda d: d.name), 
            'user': sorted(list(user_worksets.values()), key=lambda d: d.name) if user_worksets else []}


@router.get("/{imported_id}/metadata", response_model_exclude_defaults=True)
@cache()
async def get_workset_metadata(imported_id: str, workset_manager: WorksetManager, user_access_token: Annotated[str | None, Depends(get_user_access_token)]) -> WorksetInfo:
    public_workset = True
    print("get_workset_metadata()")
    print(imported_id)
    print(workset_manager)
    print(user_access_token)
    imported_id_mapping = await WorksetIdMapping.from_mongo(
        mongo_client.db["id-mappings"].find({"importedId": UUID(imported_id)}).to_list(1000))
    print(imported_id_mapping)
    if len(imported_id_mapping):
        print("A")
        imported_id_mapping = imported_id_mapping[0]
        ef_wsid = imported_id_mapping.workset_id
    else:
        print("B")
        try:
            imported_volumes = await workset_manager.get_public_workset_volumes(imported_id)
        except:
            public_workset = False
            imported_volumes = await workset_manager.get_user_workset_volumes(imported_id,user_access_token)
        print(imported_volumes)
        ef_wsid = await ef_api.create_workset(' '.join(imported_volumes))
        mongo_client.db["id-mappings"].insert_one({"importedId": UUID(imported_id), "worksetId": ef_wsid})

    volumes = await ef_api.get_workset_metadata(ef_wsid)
    if public_workset:
        workset = (await workset_manager.get_public_worksets())[imported_id]
    else:
        workset = (await workset_manager.get_user_worksets(user_access_token))[imported_id]
    if not workset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workset not found")
    volumes_meta = [torchlite_volume_meta_from_ef(vol) for vol in volumes]
    workset_info = WorksetInfo.model_construct(**workset.model_dump(), volumes=volumes_meta)
    return workset_info
