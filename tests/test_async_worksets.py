import pytest
import asyncio
import app.persisters as persisters

import app.models.torchlite as torchlite
from redis import asyncio as redis


def test_workset() -> None:
    dev_pool: redis.ConnectionPool = redis.ConnectionPool(host="localhost", port=6379, db=0)
    db: redis.Redis = redis.Redis(connection_pool=dev_pool)
    loop = asyncio.get_event_loop()

    htid = 'mdp.35112103187797'
    wsid = '6416163a2d0000f9025c8284'

    p = persisters.WorksetPersister(db)

    ws = torchlite.Workset(wsid, name="sample workset", description="only for development and testing")
    assert len(ws.volumes) == 4

    ws.disable_volume(htid)
    loop.run_until_complete(p.persist(ws))

    w2 = loop.run_until_complete(p.retrieve(ws.id))
    assert len(w2.volumes) == 3
