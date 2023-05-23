from typing import Any
from fastapi import APIRouter, Depends
from app.persisters import WorksetPersister
from app.models import torchlite as torchlite
from app.models import db as db
from app.database import get_db
import redis.asyncio as redis
import json


class WorksetPersistenceError(Exception):
    """Persistence error of some kind"""

    pass


router: APIRouter = APIRouter(prefix="/worksets", tags=["worksets"], responses={404: {"description": "Not found"}})


def pack(self, workset: torchlite.Workset) -> db.Workset:
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


@router.get("/", tags=["worksets"], response_model=None)
async def read_worksets(db: redis.Redis = Depends(get_db)) -> Any:
    db_data: dict = db.hgetall("worksets")
    data = []
    for _, v in db_data.items():
        thing = json.loads(v)
        ws: torchlite.Workset = unpack(json.loads(v))

        data.append(ws)
    return data


@router.get("/{key}", tags=["worksets"], response_model=None)
async def read_workset(key: str, db: redis.Redis = Depends(get_db)) -> Any:
    db_data: bytes | None = db.hget("worksets", key)
    if db_data is None:
        raise WorksetPersistenceError(f"could not retrieve {key} from database")

    data: dict = json.loads(db_data)
    return unpack(data)


async def read_workset_foo(key: str, db: redis.Redis = Depends(get_db)) -> Any:
    db_data: bytes | None = db.hget("worksets", key)
    if db_data is None:
        raise WorksetPersistenceError(f"could not retrieve {key} from database")

    data: dict = json.loads(db_data)
    return unpack(data)


async def read_worksets_old(db: redis.Redis = Depends(get_db)) -> Any:
    mydb = db
    db_data = mydb.hgetall("worksets")
    return db_data
