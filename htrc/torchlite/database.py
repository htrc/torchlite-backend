from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database

from htrc.torchlite.config import config


def get_database(url: str) -> Database:
    client = AsyncIOMotorClient(url)
    return client.get_default_database()


db = get_database(config.MONGODB_URL)
