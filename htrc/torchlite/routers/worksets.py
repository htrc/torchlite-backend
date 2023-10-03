from http import HTTPStatus

from fastapi import APIRouter

from ..data import worksets, get_workset_info
from ..models.schemas import WorksetSummary, WorksetInfo

router = APIRouter(
    prefix="/worksets",
    tags=["worksets"],
    responses={
        HTTPStatus.NOT_FOUND: {
            "description": "Not found"
        }
    }
)


@router.get("/")
async def list_worksets(author: str | None = None) -> list[WorksetSummary]:
    return list(worksets.values())


@router.get("/{workset_id}/metadata")
async def get_workset_metadata(workset_id: str) -> WorksetInfo:
    workset_info = get_workset_info(workset_id)
    return workset_info
