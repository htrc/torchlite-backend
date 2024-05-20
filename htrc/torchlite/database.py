from fastapi_healthchecks.checks import Check, CheckResult
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
from pymongo.server_api import ServerApi

from htrc.torchlite.config import config


class MongoDatabaseClient:
    class HealthCheck(Check):
        def __init__(self, mongo_cli):
            self.mongo_cli = mongo_cli

        async def __call__(self) -> CheckResult:
            try:
                await self.mongo_cli.ping()
            except Exception as e:
                return CheckResult(name="MongoDB", passed=False, details=str(e))
            else:
                return CheckResult(name="MongoDB", passed=True)

    class __Instance:
        def __init__(self, url: str):
            self.client = AsyncIOMotorClient(url, server_api=ServerApi('1'), uuidRepresentation='standard')
            self.db = self.client.get_default_database()

    instance = None

    def __init__(self, url: str):
        self.url = url
        self.health_check = self.HealthCheck(self)

    @property
    def db(self) -> Database:
        if not self.instance:
            self.instance = self.__Instance(self.url)

        return self.instance.db

    @property
    def client(self) -> AsyncIOMotorClient:
        if not self.instance:
            self.instance = self.__Instance(self.url)

        return self.instance.client

    async def ping(self):
        if not self.instance:
            self.instance = self.__Instance(self.url)

        await self.instance.client.admin.command("ping")

    def close(self):
        if self.instance:
            self.instance.client.close()


mongo_client = MongoDatabaseClient(config.MONGODB_URL)
