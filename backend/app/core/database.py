import ssl

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

settings = get_settings()


def _get_database_url() -> str:
    """Normalize database URL for SQLAlchemy async compatibility."""
    url = settings.database_url
    # Neon and some providers use postgres:// but SQLAlchemy needs postgresql+asyncpg://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


def _get_connect_args() -> dict:
    """Return SSL args for cloud providers (Neon, etc.)."""
    url = settings.database_url
    if "neon.tech" in url or "neon" in url:
        # Neon requires SSL
        ssl_context = ssl.create_default_context()
        return {"ssl": ssl_context}
    return {}


database_url = _get_database_url()
connect_args = _get_connect_args()

engine = create_async_engine(
    database_url,
    echo=False,
    pool_size=5,
    max_overflow=10,
    connect_args=connect_args,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
