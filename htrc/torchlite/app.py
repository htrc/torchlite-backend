import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_healthchecks.api.router import HealthcheckRouter, Probe
import redis.asyncio as redis

from .config import config
from .database import mongo_client
from .http_client import http
from .middleware import TorchliteVersionHeaderMiddleware, TimingMiddleware
from .routers.dashboards import router as dashboards_router
from .routers.worksets import router as worksets_router
from .splash import print_splash
from .version import VERSION

log = logging.getLogger(config.PROJECT_NAME)


async def torchlite_startup() -> redis.Redis:
    print_splash()
    env = os.environ.get("ENV", "dev")
    log.info(f"Starting Torchlite API Server v{VERSION} ({env})")

    # Setup backend caching
    try:
        redis_connection = redis.Redis(host=config.REDIS_HOST,port=config.REDIS_PORT,password=config.REDIS_PASSWORD,db=config.REDIS_DB)
        log.info(f"Ping successful: {await redis_connection.ping()}")
        FastAPICache.init(RedisBackend(redis_connection), enable=config.ENABLE_CACHE, expire=config.CACHE_EXPIRE, cache_status_header=config.CACHE_STATUS_HEADER)
        log.info('Cache initialized successfully')
    except Exception as e:
        log.error(f'Error initializing cache {e}')

    # ensure DB is alive
    await mongo_client.ping()

    # config_file_name = os.getenv("TORCHLITE_CONFIG")
    # if not config_file_name:
    #     raise TorchliteError("TORCHLITE_CONFIG value is invalid or not set")
    #
    # log.info(f"Loading configuration from {config_file_name}...")

    return redis_connection


async def torchlite_shutdown(redis_connection: redis.Redis):
    log.info("Server shutting down")
    await http.aclose()
    await redis_connection.aclose()
    mongo_client.close()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    redis_connection = await torchlite_startup()
    yield
    await torchlite_shutdown(redis_connection)


api = FastAPI(
    title="Torchlite API",
    version=VERSION,
    lifespan=lifespan,
)
api.include_router(worksets_router)
api.include_router(dashboards_router)
api.include_router(
    HealthcheckRouter(
        Probe(
            name="readiness",
            checks=[
                mongo_client.health_check
            ],
        ),
        Probe(
            name="liveness",
            checks=[
                mongo_client.health_check
            ],
        ),
    ),
    prefix="/health",
)
api.add_middleware(TorchliteVersionHeaderMiddleware)
api.add_middleware(TimingMiddleware)
