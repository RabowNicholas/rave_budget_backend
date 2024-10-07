# env.py

from os import environ
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

from app.database import Base
from app.models import *


load_dotenv()

# Alembic Config object
config = context.config


target_metadata = Base.metadata


def run_migrations_online():
    """Run migrations in 'online' mode."""
    section = config.get_section(config.config_ini_section)

    # Determine the database to connect to
    db_name = environ.get("DB_NAME")  # This should be set to either 'test' or 'prod'

    if db_name not in ["test", "prod"]:
        raise ValueError("DB_NAME must be either 'test' or 'prod'")

    # Inject environment variable values into connection string
    url = section["sqlalchemy.url"]

    # Adjust connection string for PostgreSQL if using 'prod'
    if db_name == "prod":
        url = url  # Use the PostgreSQL URL directly from the config
    elif db_name == "test":
        url = section["sqlalchemy.url"]  # Use the SQLite URL directly from the config

    section["sqlalchemy.url"] = url

    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
