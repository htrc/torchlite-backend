from typing import Any
import json
import config
from app.models import db, torchlite
from redis import Redis


class Persister:
    def __init__(self) -> None:
        self._db: Redis = config.db

    def persist(self, object):
        pass


class WorksetPersister(Persister):
    def __init__(self) -> None:
        super().__init__()

    def persist(self, workset: torchlite.Workset) -> str:
        db_object: db.Workset = db.Workset(
            id=workset.id, ef_id=workset.ef_id, name=workset.name, description=workset.description
        )
        if workset.volumes:
            db_object.volumes = [v.htid for v in workset.volumes]
        if workset._disabled_volumes:
            db_object.disabled_volumes = [v.htid for v in workset._disabled_volumes]

        config.db.hset("worksets", workset.id, json.dumps(db_object.dict()))
        return workset.id

    def retrieve(self, key: str) -> torchlite.Workset | None:
        db_data: bytes = config.db.hget("worksets", key)
        data: dict = json.loads(db_data)
        db_object: db.Workset = db.Workset(**data)
        workset = torchlite.Workset(ef_wsid=db_object.ef_id, name=db_object.name, description=db_object.description)
        workset.id = db_object.id

        if data['disabled_volumes']:
            workset._disabled_volumes = [torchlite.Volume(htid) for htid in data['disabled_volumes']]
        if data['volumes']:
            workset.volumes = [torchlite.Volume(htid) for htid in data['volumes']]

        return workset


"""This is obsolete now; we should be persisting torchlite objects"""


class DashboardPersister(Persister):
    def __init__(self) -> None:
        super().__init__()

    def persist(self, dashboard: db.Dashboard) -> None:
        print("persisting")
        if dashboard.dict():
            config.db.hset("dashboards", dashboard.id, json.dumps(dashboard.dict()))
            print("persisted")
        else:
            print("nothing to persist")

    def retrieve(self, id: str) -> db.Dashboard:
        db_data: Any = self._db.hget("dashboards", id)
        data: dict = json.loads(db_data)
        return db.Dashboard(**data)
