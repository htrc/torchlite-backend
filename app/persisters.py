from typing import Any
import json
import config
from app.models import db, torchlite
from redis import Redis


class PersistenceError(Exception):
    """Persistence error of some kind"""

    pass


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
        db_data: bytes | None = config.db.hget("worksets", key)
        if db_data is None:
            raise PersistenceError(f"could not retrieve {key} from database")

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

    def persist(self, dashboard: torchlite.Dashboard) -> str:
        db_object: db.Dashboard = db.Dashboard(id=dashboard.id, name=dashboard.name)
        if dashboard.workset:
            db_object.workset = dashboard.workset.id

        config.db.hset("dashboards", dashboard.id, json.dumps(db_object.dict()))
        return dashboard.id

    def retrieve(self, key: str) -> torchlite.Dashboard | None:
        db_data: bytes | None = config.db.hget("dashboards", key)

        if db_data is None:
            raise PersistenceError(f"could not retrieve {key} from database")

        data: dict = json.loads(db_data)
        db_object: db.Dashboard = db.Dashboard(**data)

        dashboard: torchlite.Dashboard = torchlite.Dashboard(name=db_object.name)
        dashboard.id = db_object.id
        if db_object.workset:
            wsp = WorksetPersister()
            ws = wsp.retrieve(db_object.workset)
            dashboard.workset = ws
        return dashboard
