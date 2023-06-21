from typing import Any
from redis import asyncio as redis
import json
from app.models import db, torchlite


class PersistenceError(Exception):
    """Persistence error of some kind"""

    pass


class Persister:
    def __init__(self, db: redis.Redis) -> None:
        self.db: redis.Redis = db

    def persist(self, object):
        pass


class WorksetPersister(Persister):
    def __init__(self, db: redis.Redis) -> None:
        super().__init__(db)

    def pack(self, workset: torchlite.Workset) -> db.Workset:
        db_object: db.Workset = db.Workset(
            id=workset.id, ef_id=workset.ef_id, name=workset.name, description=workset.description
        )
        if workset.volumes:
            db_object.volumes = [v.htid for v in workset.volumes]
        # if workset._disabled_volumes:
        #     db_object.disabled_volumes = [v.htid for v in workset._disabled_volumes]
        return db_object

    def unpack(self, data: dict) -> torchlite.Workset:
        db_object: db.Workset = db.Workset(**data)
        workset = torchlite.Workset(ef_wsid=db_object.ef_id, name=db_object.name, description=db_object.description)
        workset.id = db_object.id

        # if data['disabled_volumes']:
        #     workset._disabled_volumes = [torchlite.Volume(htid) for htid in data['disabled_volumes']]
        if data["volumes"]:
            workset.volumes = [torchlite.Volume(htid) for htid in data["volumes"]]

        return workset

    async def persist(self, workset: torchlite.Workset) -> str:
        db_object = self.pack(workset)
        await self.db.hset("worksets", workset.id, json.dumps(db_object.dict()))
        return workset.id

    async def retrieve(self, key: str) -> torchlite.Workset | None:
        db_data: bytes | None = await self.db.hget("worksets", key)
        if db_data is None:
            raise PersistenceError(f"could not retrieve {key} from database")

        data: dict = json.loads(db_data)
        workset = self.unpack(data)
        return workset

    async def retrieve_all(self) -> list[torchlite.Workset] | None:
        db_data: Any = await self.db.hgetall("worksets")
        if db_data is None:
            raise PersistenceError("could not retrieve anythinng from database")

        workset_list = []
        for k, v in db_data():
            thing = json.loads(v)
            workset: torchlite.Workset = self.unpack(thing)
            workset_list.append(workset)
        return workset_list

    async def retrieve_all_old(self) -> list[torchlite.Workset] | None:
        db_data: Any = await self.db.hgetall("worksets")
        if db_data is None:
            raise PersistenceError("could not retrieve anythinng from database")

        data: dict = json.loads(db_data)
        return_list = []
        for k, v in data.items():
            workset: torchlite.Workset = self.unpack(v)
            return_list.append(workset)
        return return_list


# class DashboardPersister(Persister):
#     def __init__(self, db: redis.Redis) -> None:
#         super().__init__(db)

#     async def persist(self, dashboard: torchlite.Dashboard) -> str:
#         db_object: db.Dashboard = db.Dashboard(id=dashboard.id, name=dashboard.name)
#         if dashboard.workset:
#             db_object.workset = dashboard.workset.id

#         await self.db.hset("dashboards", dashboard.id, json.dumps(db_object.dict()))
#         return dashboard.id

#     async def retrieve(self, key: str) -> torchlite.Dashboard | None:
#         db_data: bytes | None = await self.db.hget("dashboards", key)

#         if db_data is None:
#             raise PersistenceError(f"could not retrieve {key} from database")

#         data: dict = json.loads(db_data)
#         db_object: db.Dashboard = db.Dashboard(**data)

#         dashboard: torchlite.Dashboard = torchlite.Dashboard(name=db_object.name)
#         dashboard.id = db_object.id

#         if db_object.workset:
#             wsp = WorksetPersister(self.db)
#             ws = await wsp.retrieve(db_object.workset)
#             dashboard.workset = ws

#         return dashboard
