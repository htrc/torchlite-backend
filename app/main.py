import os
from pathlib import Path
from typing import Optional, AsyncGenerator
from urllib.parse import urlparse, ParseResult
from contextlib import asynccontextmanager
from dotenv import load_dotenv, find_dotenv
import requests
from yaml import safe_load
from fastapi import FastAPI
from app.config import persistence_db_pool
from app.routers.worksets import router as workset_router
from app.routers.data import router as data_router


class TorchliteError(Exception):
    """Torchlite error of some kind"""

    pass


async def torchlite_startup() -> None:
    config_file_name: Optional[str] = os.getenv("TORCHLITE_CONFIG")
    if not config_file_name:
        raise TorchliteError("TORCHLITE_CONFIG value is invalid or not set")

    print(f"Loading configuration from {config_file_name}...")
    parse_result: ParseResult = urlparse(config_file_name)

    if parse_result.scheme.startswith("http"):
        resp: requests.Response = requests.get(config_file_name)
        if resp.status_code == 200:
            safe_load(resp.text)
        else:
            raise TorchliteError(f"Could not load config {config_file_name} - HTTP error {resp.status_code}")
    else:
        p: Path = Path(parse_result.path)
        try:
            with open(p, mode="r", encoding="utf-8-sig") as f:
                safe_load(f)
        except IOError as e:
            raise TorchliteError(f"could not load config file {config_file_name}") from e


async def torchlite_shutdown() -> None:
    persistence_db_pool.disconnect()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await torchlite_startup()

    yield

    await torchlite_shutdown()


if find_dotenv() is False:
    raise TorchliteError("could not load .env file")

load_dotenv(find_dotenv())


app = FastAPI(lifespan=lifespan)

app.include_router(workset_router)
app.include_router(data_router)
