from typing import Any
from fastapi import APIRouter, Depends
from app.persisters import WorksetPersister
from app.database import get_db
import redis.asyncio as redis

router: APIRouter = APIRouter(prefix="/worksets", tags=["worksets"], responses={404: {"description": "Not found"}})


@router.get("/", tags=["worksets"], response_model=None)
async def read_worksets(db: redis.Redis = Depends(get_db)) -> Any:
    db_data = db.hgetall("worksets")
    return db_data
