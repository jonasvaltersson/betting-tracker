import json

import pytest
import boto3
import flask.testing
from sqlalchemy import event

from . import create_app
from . import db
from . import CONFIG

class JsonTestClient(flask.testing.FlaskClient):
    @staticmethod
    def _handle_json(kwargs):
        json_data = kwargs.pop('json', None)
        if json_data is not None:
            assert isinstance(json_data, dict)
            assert 'data' not in kwargs
            kwargs['data'] = json.dumps(json_data)
            kwargs['content_type'] = 'application/json'

    def post(self, *args, **kwargs):
        JsonTestClient._handle_json(kwargs)
        return super(JsonTestClient, self).post(*args, **kwargs)

    def put(self, *args, **kwargs):
        JsonTestClient._handle_json(kwargs)
        return super(JsonTestClient, self).put(*args, **kwargs)


class JsonResponse(flask.wrappers.Response):
    
    @property
    def json(self):
        return json.loads(self.data.decode('utf-8'))


@pytest.fixture(scope='session')
def test_client(db_test_setup):
    connexion_app = create_app(db_test_setup)
    connexion_app.app.test_client_class = JsonTestClient
    connexion_app.app.testing = True
    connexion_app.app.response_class = JsonResponse
    return connexion_app.app.test_client()


@pytest.fixture(scope='session')
def db_test_setup():
    db_uri = 'postgresql+psycopg2://'
    db.init_engine(
        db_uri,
        db_host=CONFIG['app_db_host'],
        db_port=CONFIG['app_db_port'],
        db_name=CONFIG['app_db_name'],
        db_user=CONFIG['app_db_user'],
        echo=None,
        db_password=CONFIG['app_db_password'])
    db.wait_for_it()
    db.drop_all()
    db.create_all()
    yield db
    db.drop_all()


@pytest.fixture(scope='session')
def db_conn(db_test_setup):
    conn = db.engine.connect()
    yield conn
    conn.close()


@pytest.fixture(scope='function', autouse=True)
def db_session(db_conn):
    """Creates a new database session for each test."""
    db.Session.remove()
    transaction = db_conn.begin()  # begin non-ORM transaction
    db.Session.configure(bind=db_conn)
    sess = db.Session()

    sess.begin_nested()  # start session in a SAVEPOINT

    # each time the savepoint ends, re-open it
    @event.listens_for(sess, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            # ensure that state is expired the way
            # session.commit() at the top level normally does
            # (optional step)
            session.expire_all()
            session.begin_nested()

    yield sess
    sess.close()
    transaction.rollback()  # clean-up everything after test


@pytest.fixture(autouse=True)
def transaction(db_session):
    pass


@pytest.fixture(autouse=True)
def flask_app():
    connexion_app = create_app()
    return connexion_app.app

