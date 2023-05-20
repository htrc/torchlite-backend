import config
import app.models.db as db
from app.services.ef_api import EFApi
import persisters
import models.torchlite as torchlite

d1 = db.Dashboard()

p = persisters.DashboardPersister()

htid = 'mdp.39015058744122'
wsid = '6416163a2d0000f9025c8284'

ws = torchlite.Workset(wsid, name="sample workset", description="only for development and testing")

# api = EFApi()
# tokens = api.tokens(htid)

p = persisters.WorksetPersister()
key = p.persist(ws)

ws2 = p.retrieve(key)

ws.disable_volume('mdp.35112103187797')
p.persist(ws)
w3 = p.retrieve(ws.id)

dashboard = torchlite.Dashboard(name="a sample dashboard")
dashboard.workset = w3
persisters.DashboardPersister().persist(dashboard)
