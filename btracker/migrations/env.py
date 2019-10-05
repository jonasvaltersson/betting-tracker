import logging
import sys

import app # noqa
from alembic import context

# append path to be able to import app
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# NOTE: Model metadata imported here only for supporting the *autogeneration*
# of migrations. Models will never be invoked as part of normal migration
# execution.
from app import persistence, BASE_DB_URI   # noqa
target_metadata = app.db.Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """


    CONFIG = dict(
        app_db_host='storage',
        app_db_port='5432',
        app_db_name='btracker_db',
        app_db_user='postgres',
        app_db_password='password',
        app_db_conn_pool_size=10,
        environment='test'
    )

    connectable = app.db.init_engine(
        BASE_DB_URI,
        db_host=CONFIG['app_db_host'],
        db_port=CONFIG['app_db_port'],
        db_user=CONFIG['app_db_user'],
        db_name=CONFIG['app_db_name'],
        db_password=CONFIG['app_db_password']
    )

    app.db.wait_for_it()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
