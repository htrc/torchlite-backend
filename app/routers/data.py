from typing import Any
from fastapi import APIRouter, Depends
import redis.asyncio as redis
from app.models import torchlite as torchlite
from app.config import get_db
from app.widgets import MapWidget, TimelineWidget
from app.routers.worksets import read_workset


router: APIRouter = APIRouter(prefix="/data", tags=["data"], responses={404: {"description": "Not found"}})


@router.get("/map", tags=["data"], response_model=None)
async def get_map_data(workset_id: str, db: redis.Redis = Depends(get_db)) -> Any:
    workset = await read_workset(workset_id, db)
    widget = MapWidget(workset)
    return widget.data()


@router.get("/timeline", tags=["data"], response_model=None)
async def get_timeline_data(workset_id: str, db: redis.Redis = Depends(get_db)) -> Any:
    workset = await read_workset(workset_id, db)
    widget = TimelineWidget(workset)
    return widget.data()
