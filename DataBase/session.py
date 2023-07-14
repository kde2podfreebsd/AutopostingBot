import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

# sqlalchemy.url = postgresql://postgres:postgres@172.20.0.2:5432/postgres

# from DataBase.Models import Models
# target_metadata = Models.Base.metadata

POSTGRES_USER = str(os.getenv("POSTGRES_USER"))
POSTGRES_PASSWORD = str(os.getenv("POSTGRES_PASSWORD"))
POSTGRES_HOST = str(os.getenv("POSTGRES_HOST"))
POSTGRES_PORT = str(os.getenv("POSTGRES_PORT"))
POSTGRES_DB = str(os.getenv("POSTGRES_DB"))

REAL_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
print(REAL_DATABASE_URL)

engine = create_async_engine(
    REAL_DATABASE_URL,
    future=True,
    echo=False,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

async_session = async_sessionmaker(engine, expire_on_commit=True, class_=AsyncSession)


async def get_db() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
