from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database

from htrc.torchlite.config import config


class MongoDatabaseClient:
    class __Instance:
        def __init__(self, url: str):
            self.client = AsyncIOMotorClient(url)
            self.db = self.client.get_default_database()

    instance = None

    def __init__(self, url: str):
        self.url = url

    @property
    def db(self) -> Database:
        if not self.instance:
            self.instance = self.__Instance(self.url)

        return self.instance.db

    async def ping(self):
        if not self.instance:
            self.instance = self.__Instance(self.url)

        self.instance.client.admin.command("ping")

    def close(self):
        if self.instance:
            self.instance.client.close()


mongo_client = MongoDatabaseClient(config.MONGODB_URL)
