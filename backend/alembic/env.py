import asyncio
import os
import ssl
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.database import Base
from app.models import Document, Job  # noqa: F401

config = context.config

# Override sqlalchemy.url from DATABASE_URL env var if available
database_url = os.environ.get("DATABASE_URL")
if database_url:
    # Neon and some providers use postgres:// but SQLAlchemy needs postgresql+asyncpg://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif database_url.startswith("postgresql://") and not database_url.startswith("postgresql+"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    # Remove query params not supported by asyncpg (sslmode, channel_binding)
    if "?" in database_url:
        database_url = database_url.split("?")[0]
    config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    # Add SSL for Neon/cloud providers
    connect_args = {}
    db_url = os.environ.get("DATABASE_URL", "")
    if "neon.tech" in db_url or "neon" in db_url:
        ssl_context = ssl.create_default_context()
        connect_args = {"ssl": ssl_context}

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
