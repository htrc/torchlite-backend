import config
import app.models.db as db
import persisters
import models.torchlite as torchlite

d1 = db.Dashboard()

p = persisters.DashboardPersister()

htid = 'mdp.39015058744122'
wsid = '6416163a2d0000f9025c8284'

ws = torchlite.Workset(wsid)
