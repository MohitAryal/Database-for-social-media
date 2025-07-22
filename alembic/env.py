import asyncio
from logging.config import fileConfig
import os

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load Alembic config
config = context.config
fileConfig(config.config_file_name)

# Get metadata for 'autogenerate' support
from app.models import Base  # Update this import based on your project structure
target_metadata = Base.metadata

# Load database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable not set")

# Run migrations in 'offline' mode
def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# Run migrations in 'online' mode
def run_migrations_online():
    connectable: AsyncEngine = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async def do_migrations(connection):
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
            )
        )
        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(
        connectable.connect().run_sync(do_migrations)
    )

# Entry point
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()