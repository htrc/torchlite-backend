import redis
from app.services.ef_api import EFApi
from app.database import dev_db, test_db, prod_db


db = dev_db
ef_api = EFApi()
