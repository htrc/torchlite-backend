from typing import Any
import redis.asyncio as redis
import json
from fastapi import APIRouter, Depends
from app.persisters import WorksetPersister
from app.services.ef_api import EFApi
from app.models import torchlite as torchlite
from app.models import db as db
from app.config import get_db


class WorksetPersistenceError(Exception):
    """Persistence error of some kind"""

    pass


router: APIRouter = APIRouter(prefix="/worksets", tags=["worksets"], responses={404: {"description": "Not found"}})


def pack(workset: torchlite.Workset) -> db.Workset:
    db_object: db.Workset = db.Workset(
        id=workset.id, ef_id=workset.ef_id, name=workset.name, description=workset.description
    )
    if workset.volumes:
        db_object.volumes = [v.htid for v in workset.volumes]
    if workset._disabled_volumes:
        db_object.disabled_volumes = [v.htid for v in workset._disabled_volumes]
    return db_object


def unpack(data: dict) -> torchlite.Workset:
    db_object: db.Workset = db.Workset(**data)
    workset = torchlite.Workset(ef_wsid=db_object.ef_id, name=db_object.name, description=db_object.description)
    workset.id = db_object.id

    if data['disabled_volumes']:
        workset._disabled_volumes = [torchlite.Volume(htid) for htid in data['disabled_volumes']]
        if data['volumes']:
            workset.volumes = [torchlite.Volume(htid) for htid in data['volumes']]
    return workset


async def load(wsid: str, db: redis.Redis) -> torchlite.Workset:
    db_data: Any = db.hget("worksets", wsid)
    if db_data is None:
        raise WorksetPersistenceError(f"could not retrieve {wsid} from database")
    data: dict = json.loads(db_data)
    workset: torchlite.Workset = unpack(data)
    return workset


async def store(workset: torchlite.Workset, db: redis.Redis) -> None:
    db_object = pack(workset)
    db.hset("worksets", workset.id, json.dumps(db_object.dict()))


@router.get("/", tags=["worksets"], response_model=None)
async def read_worksets(db: redis.Redis = Depends(get_db)) -> Any:
    db_data: Any = db.hgetall("worksets")
    data = []
    for _, v in db_data.items():
        ws: torchlite.Workset = unpack(json.loads(v))

        data.append(ws)
    return data


@router.get("/{wsid}", tags=["worksets"], response_model=None)
async def read_workset(wsid: str, db: redis.Redis = Depends(get_db)) -> Any:
    return await load(wsid, db)


@router.delete("/{wsid}/{htid}", tags=["worksets"], response_model=None)
async def remove_volume(wsid: str, htid: str, db: redis.Redis = Depends(get_db)) -> None:
    workset: torchlite.Workset = await load(wsid, db)
    workset.remove_volume(htid)
    return await store(workset, db)


@router.put("/{wsid}/{htid}", tags=["worksets"], response_model=None)
async def add_volume(wsid: str, htid: str, db: redis.Redis = Depends(get_db)) -> None:
    workset: torchlite.Workset = await load(wsid, db)
    workset.add_volume(htid)
    return await store(workset, db)


@router.post("/{ef_wsid}", tags=["worksets"], response_model=None)
async def create_workset(ef_wsid: str, db: redis.Redis = Depends(get_db)) -> str:
    workset: torchlite.Workset = torchlite.Workset(ef_wsid=ef_wsid)
    await store(workset, db)
    return workset.id
