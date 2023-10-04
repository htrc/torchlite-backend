from uuid import UUID

from authlib.oidc.core import UserInfo
from fastapi import APIRouter, Depends, HTTPException, status

from ..auth.auth import get_current_user
from ..config import config
from ..database import mongo_client
from ..models.schemas import DashboardSummary, DashboardPatch

router = APIRouter(
    prefix="/dashboards",
    tags=["dashboards"],
)


@router.get("/")
async def list_dashboards(owner: str | None = None,
                          user: UserInfo | None = Depends(get_current_user)) -> list[DashboardSummary]:
    if owner in ["torchlite", str(config.TORCHLITE_UID)]:
        return await DashboardSummary.from_mongo(
            mongo_client.db["dashboards"].find({"owner": config.TORCHLITE_UID}).to_list(1000)
        )

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_id = UUID(user.get("htrc-guid", user.sub))
    owner = UUID(owner) if owner else user_id

    if user_id != owner:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return await DashboardSummary.from_mongo(
        mongo_client.db["dashboards"].find({"owner": owner}).to_list(1000)
    )


@router.post("/", description="Create a new dashboard")
async def create_dashboard(owner: str | None = None) -> DashboardSummary:
    dashboard = None
    return dashboard


@router.get("/{dashboard_id}")
async def get_dashboard(dashboard_id: str) -> DashboardSummary:
    pass


@router.patch("/{dashboard_id}")
async def update_dashboard(dashboard_id: str, dashboard_patch: DashboardPatch):
    pass


@router.get("/{dashboard_id}/widgets/{widget_type}/data")
async def get_widget_data(dashboard_id: str, widget_type: str):
    pass
