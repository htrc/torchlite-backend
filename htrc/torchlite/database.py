from contextlib import asynccontextmanager

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from htrc.torchlite import VERSION
from htrc.torchlite.config import config
from htrc.torchlite.models.base import Base

async_engine = create_async_engine(
    config.DB_URL,
    future=True,
    echo=config.LOCAL_DEV,
    hide_parameters=not config.LOCAL_DEV,
    pool_pre_ping=True,
    connect_args={
        # https://www.postgresql.org/docs/current/runtime-config.html
        "server_settings": {
            "application_name": f"{config.PROJECT_NAME} {VERSION} async",
            "jit": "off",
        },
    },
)

async_session = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False,
    future=True,
)


async def init_db():
    async with async_engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
