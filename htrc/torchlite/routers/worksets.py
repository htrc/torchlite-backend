from http import HTTPStatus

from fastapi import APIRouter

from ..fake import generate_workset_summary, generate_workset_info
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
    worksets = [generate_workset_summary() for _ in range(10)]
    return worksets


@router.get("/{workset_id}/metadata")
async def get_workset_metadata(workset_id: str) -> WorksetInfo:
    workset = generate_workset_info()
    return workset
