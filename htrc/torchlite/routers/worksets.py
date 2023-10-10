from fastapi import APIRouter

from ..converters import torchlite_volume_meta_from_ef
from ..data import worksets
from ..ef.api import ef_api
from ..managers.workset_manager import WorksetManager
from ..models.workset import WorksetSummary, WorksetInfo

router = APIRouter(
    prefix="/worksets",
    tags=["worksets"],
)


@router.get("/")
async def list_worksets(workset_manager: WorksetManager, author: str | None = None) -> list[WorksetSummary]:
    featured_worksets = await workset_manager.get_featured_worksets()
    return list(featured_worksets.values())


@router.get("/{workset_id}/metadata")
async def get_workset_metadata(workset_id: str) -> WorksetInfo:
    volumes = await ef_api.get_workset_metadata(workset_id)
    workset = worksets[workset_id]
    volumes_meta = [torchlite_volume_meta_from_ef(vol) for vol in volumes]
    workset_info = WorksetInfo.model_construct(**workset.model_dump(), volumes=volumes_meta)
    return workset_info
