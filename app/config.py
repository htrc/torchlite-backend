import redis
from services.ef_api import EFApi


db = redis.Redis()
ef_api = EFApi()
