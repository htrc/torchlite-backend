import redis
from services.ef_api import EFApi
from database import dev_db, test_db, prod_db


db = dev_db
ef_api = EFApi()
