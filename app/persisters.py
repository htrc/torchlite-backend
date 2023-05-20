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

    def persist(self, workst: torchlite.Workset) -> None:
        pass


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
