import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi_healthchecks.api.router import HealthcheckRouter, Probe

from .config import Config
from .database import init_db
from .middleware import TorchliteVersionHeaderMiddleware
from .routers.dashboards import router as dashboards_router
from .routers.worksets import router as worksets_router
from .splash import print_splash
from .version import VERSION

log = logging.getLogger(Config.PROJECT_NAME)


async def torchlite_startup():
    print_splash()
    env = os.environ.get("ENV", "dev")
    log.info(f"Starting Torchlite API Server v{VERSION} ({env})")

    await init_db()

    # config_file_name = os.getenv("TORCHLITE_CONFIG")
    # if not config_file_name:
    #     raise TorchliteError("TORCHLITE_CONFIG value is invalid or not set")
    #
    # log.info(f"Loading configuration from {config_file_name}...")


async def torchlite_shutdown():
    log.info("Server shutting down")
    pass


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await torchlite_startup()
    yield
    await torchlite_shutdown()

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
            checks=[],  # TBD
        ),
        Probe(
            name="liveness",
            checks=[],
        ),
    ),
    prefix="/health",
)
api.add_middleware(
    TorchliteVersionHeaderMiddleware,
)
