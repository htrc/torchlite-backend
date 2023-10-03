from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models.schemas import DashboardSummary, DashboardPatch

router = APIRouter(
    prefix="/dashboards",
    tags=["dashboards"],
    responses={
        HTTPStatus.NOT_FOUND: {
            "description": "Not found"
        }
    }
)


@router.get("/")
async def list_dashboards(owner: str | None = None,
                          session: AsyncSession = Depends(get_session)) -> list[DashboardSummary]:
    dashboards = []
    return dashboards


@router.post("/")
async def create_dashboard(owner: str | None = None,
                           session: AsyncSession = Depends(get_session)) -> DashboardSummary:
    dashboard = None
    return dashboard


@router.get("/{dashboard_id}")
async def get_dashboard(dashboard_id: str,
                        session: AsyncSession = Depends(get_session)) -> DashboardSummary:
    pass


@router.patch("/{dashboard_id}")
async def update_dashboard(dashboard_id: str,
                           dashboard_patch: DashboardPatch,
                           session: AsyncSession = Depends(get_session)):
    pass


@router.get("/{dashboard_id}/widgets/{widget_type}/data")
async def get_widget_data(dashboard_id: str, widget_type: str,
                          session: AsyncSession = Depends(get_session)):
    pass
