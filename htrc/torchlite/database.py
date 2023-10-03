from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from htrc.torchlite import VERSION
from htrc.torchlite.config import Config
from htrc.torchlite.models.base import Base

async_engine = create_async_engine(
    Config.DB_URL,
    future=True,
    echo=Config.LOCAL_DEV,
    hide_parameters=not Config.LOCAL_DEV,
    pool_pre_ping=True,
    connect_args={
        # https://www.postgresql.org/docs/current/runtime-config.html
        "server_settings": {
            "application_name": f"{Config.PROJECT_NAME} {VERSION} async",
            "jit": "off",
        },
    },
)


async def init_db():
    async with async_engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncSession:
    async_session = async_sessionmaker(
        bind=async_engine,
        autoflush=False,
        expire_on_commit=False,
        future=True,
    )
    async with async_session() as session:
        yield session
