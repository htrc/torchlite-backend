from fastapi import APIRouter
from uuid import UUID

from ..converters import torchlite_volume_meta_from_ef
from ..ef.api import ef_api
from ..managers.workset_manager import WorksetManager
from ..models.workset import WorksetSummary, WorksetInfo, WorksetIdMapping
from ..database import mongo_client

router = APIRouter(
    prefix="/worksets",
    tags=["worksets"],
)


@router.get("/", response_model_exclude_defaults=True)
async def list_worksets(workset_manager: WorksetManager, author: str | None = None) -> dict[str, list[WorksetSummary]]:
    public_worksets = await workset_manager.get_public_worksets()
    featured_worksets = workset_manager.get_featured_worksets()

    return { 'public': sorted(list(public_worksets.values()),key=lambda d: d.name), 'featured': sorted(list(featured_worksets.values()),key=lambda d: d.name)}


@router.get("/{imported_id}/metadata", response_model_exclude_defaults=True)
async def get_workset_metadata(imported_id: str, workset_manager: WorksetManager) -> WorksetInfo:
#    print("GETTING WORKSET METADATA FOR")
#    print(imported_id)
    imported_id_mapping = (await WorksetIdMapping.from_mongo(mongo_client.db["id-mappings"].find({"importedId": UUID(imported_id)}).to_list(1000)))[0]
#    print(imported_id_mapping)
#    print(imported_id_mapping.workset_id)
    volumes = await ef_api.get_workset_metadata(imported_id_mapping.workset_id)
#    print(volumes)
    workset = (await workset_manager.get_public_worksets())[imported_id]
#    print(workset)
    volumes_meta = [torchlite_volume_meta_from_ef(vol) for vol in volumes]
    workset_info = WorksetInfo.model_construct(**workset.model_dump(), volumes=volumes_meta)
#    print(workset_info)
    return workset_info
