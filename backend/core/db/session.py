from contextlib import asynccontextmanager, contextmanager
from core.utils.conf import CoreSettings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker


def __get_conn_str() -> str:
    settings = CoreSettings()
    user = settings.postgres_user
    pwd = settings.postgres_password
    db = settings.postgres_db
    host = settings.postgres_host
    return f"postgresql://{user}:{pwd}@{host}/{db}"


def __get_async_conn_str() -> str:
    settings = CoreSettings()
    user = settings.postgres_user
    pwd = settings.postgres_password
    db = settings.postgres_db
    host = settings.postgres_host
    return f"postgresql+asyncpg://{user}:{pwd}@{host}/{db}"


__ENGINE = create_engine(__get_conn_str())
__ASYNC_ENGINE = create_async_engine(__get_async_conn_str())
__SESSION_MAKER = sessionmaker(__ENGINE)
__ASYNC_SESSION_MAKER = async_sessionmaker(__ASYNC_ENGINE, expire_on_commit=False)


def get_engine():
    return __ENGINE


@contextmanager
def get_session():
    with __SESSION_MAKER() as session:
        with session.begin():
            yield session


@asynccontextmanager
async def get_async_session():
    async with __ASYNC_SESSION_MAKER() as session:
        async with session.begin():
            yield session
