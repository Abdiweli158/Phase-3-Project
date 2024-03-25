from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import the SQLAlchemy Base object from your main module
from main import Base

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Set up logging configuration if a config file name is provided
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata for migrations to the Base metadata from SQLAlchemy
target_metadata = Base.metadata

# Define a function to run migrations in 'offline' mode
def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine,
    although an Engine is acceptable here as well.
    By skipping the Engine creation, we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Define a function to run migrations in 'online' mode
def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario, we need to create an Engine and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine whether to run migrations in offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
