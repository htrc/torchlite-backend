from http import HTTPStatus

from fastapi import APIRouter

from ..database import db
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
async def list_dashboards(owner: str | None = None) -> list[DashboardSummary]:
    dashboards = []
    return dashboards


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
