"""Alembic environment configuration for database migrations."""

import logging
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

# Import ALL models to register them with SQLModel.metadata
from yubal_api.db.settings import AppSetting  # noqa: F401
from yubal_api.db.subscription import Subscription  # noqa: F401
from yubal_api.settings import get_settings

config = context.config
settings = get_settings()

# Set URL dynamically from settings and ensure directory exists
settings.db_path.parent.mkdir(parents=True, exist_ok=True)
config.set_main_option("sqlalchemy.url", f"sqlite:///{settings.db_path}")

# Only configure logging from alembic.ini if not already configured.
# When running programmatically (via app.py), logging is already set up.
# This prevents alembic from overwriting the app's log level configuration.
if config.config_file_name is not None and not logging.root.handlers:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
