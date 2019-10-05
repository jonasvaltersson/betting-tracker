import logging

import alembic.config
import psycopg2
import os
import time

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func



engine = None

CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=CONVENTION)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(session_factory)
LOGGER = logging.getLogger(__name__)


class CustomBase:

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    query = Session.query_property()

    def save(self):
        Session().add(self)
        try:
            Session().commit()
        except:  # noqa: E722
            Session().rollback()
            raise

    def to_dict(self):
        dct = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if value is None:
                continue
            dct[column.name] = getattr(self, column.name)
        return dct


Base = declarative_base(metadata=metadata, cls=CustomBase)


def init_engine(base_uri, db_host=None, db_port=None, db_name=None, db_user=None, db_password=None, **kwargs):
    assert db_password is not None
    global engine
    conn_factory = DBConnectionFactory(db_host, db_port, db_name, db_user, db_password)
    if engine is not None:
        logging.warning('Engine can only be initialized once. Reusing existing engine.')
    else:
        engine = create_engine(base_uri, creator=conn_factory._connect, **kwargs)
    Session.configure(bind=engine)
    return engine


def get_engine():
    return engine


def create_all():
    alembic.config.main(argv=['upgrade', 'head'])


def drop_all():
    engine.execute('DROP SCHEMA public CASCADE; CREATE SCHEMA public;')


def wait_for_it(max_wait_in_sec=20, freq=4):
    assert engine, 'Engine needs to be initialized before use'
    for i in range(max_wait_in_sec * freq):
        try:
            conn = engine.connect()
            conn.close()
            break
        except:  # noqa: E722
            time.sleep(1 / freq)


def attach_to_app(flask_app):
    """Ensure db session is removed at app/request teardown."""

    @flask_app.teardown_appcontext
    def shutdown_session(response_or_exc):
        Session.remove()
        return response_or_exc


class DBConnectionFactory:

    def __init__(self, host, port, name, user, password):
        self.host = host
        self.port = port
        self.name = name
        self.user = user
        self.password = password

    def _connect(self):
        LOGGER.info('Creating new connection...')
        import pdb; pdb.set_trace()
        return psycopg2.connect(host=self.host, dbname=self.name, port=self.port,
                                user=self.user, password=self.password)

    def _is_auth_error(self, exc):
        return 'Access denied for user' in str(exc)
