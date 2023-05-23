import os
from urllib.parse import urlparse, ParseResult
from contextlib import asynccontextmanager
from dotenv import load_dotenv, find_dotenv
import requests
from yaml import safe_load
from fastapi import FastAPI
from fastapi_healthchecks.api.router import HealthcheckRouter, Probe
from redis import asyncio as redis


import app.persisters
import app.models.db as db
import app.models.torchlite as torchlite
from app.services.ef_api import EFApi
from app.services.middleware import TorchliteVersionHeaderMiddleware
from app.routers.dashboards import router as dashboard_router
from app.routers.worksets import router as workset_router


class TorchliteError(Exception):
    """Torchlite error of some kind"""

    pass


async def torchlite_startup():
    config_file_name: Optional[str] = os.getenv("TORCHLITE_CONFIG")
    if not config_file_name:
        raise TorchliteError("TORCHLITE_CONFIG value is invalid or not set")

    print(f"Loading configuration from {config_file_name}...")
    parse_result: ParseResult = urlparse(config_file_name)

    if parse_result.scheme.startswith("http"):
        resp: requests.Response = requests.get(config_file_name)
        if resp.status_code == 200:
            config = safe_load(resp.text)
        else:
            raise TorchliteError(f"Could not load config {config_file_name} - HTTP error {resp.status_code}")
    else:
        p: Path = Path(parse_result.path)
        try:
            with open(p, mode="r", encoding="utf-8-sig") as f:
                config = safe_load(f)
        except IOError as e:
            raise TorchliteError(f"could not load config file {config_file_name}") from e

    persistence_db_pool: redis.ConnectionPool = redis.ConnectionPool(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        db=os.getenv("DB_NUMBER"),
        password=os.getenv("DB_PASSWORD"),
        ssl=os.getenv("DB_SSL"),
        minsize=os.getenv("DB_POOL_MINSIZE"),
        maxsize=os.getenv("DB_POOL_MAXSIZE"),
        encoding="utf8",
    )

    persistence_db: redis.Redis = redis.Redis(connection_pool=persistence_db_pool, auto_close_connection_pool=False)


async def torchlite_shutdown():
    await persistence_db.close()
    await persistence_db_pool.disconnect()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await torchlite_startup()

    yield

    await torchlite_shutdown()


def get_db():
    persistence_db: redis.Redis = redis.Redis(connection_pool=persistence_db_pool, auto_close_connection_pool=False)
    try:
        yield persistence_db
    finally:
        persistence_db.close()


if find_dotenv() is False:
    raise TorchliteError("could not load .env file")
load_dotenv(find_dotenv())


app = FastAPI(lifespan=lifespan)

app.include_router(dashboard_router)
app.include_router(workset_router)
