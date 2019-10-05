import connexion  # noqa
from connexion.operation import Swagger2Operation

import json  # noqa
import os  # noqa: E402
import sys  # noqa
import yaml  # noqa
import flask  # noqa
from flask_cors import CORS  # noqa

from . import db  # noqa

SERVICE_NAME = 'btracker-service'
BASE_DB_URI = 'postgresql+psycopg2://'


class TagToModuleResolver(connexion.resolver.Resolver):
    def __init__(self, tag_to_module: dict):
        self.tag_to_module = tag_to_module
        super().__init__()

    def resolve_operation_id(self, operation):
        tags = operation._operation.get('tags')

        if not self.tag_to_module or not tags:
            return operation.operation_id
        
        tag = tags[0]

        return f'{self.tag_to_module[tag]}.{operation.operation_id}'

def create_app(db_=None):
    app = connexion.App(__name__)

    app.add_api(
        'api_spec.yml',
        resolver=TagToModuleResolver({
            'btracker': 'app.endpoints'
        }),
        strict_validation=True,
        validate_responses=True
    )

    if db_:
        db_.attach_to_app(app.app)

    CORS(app.app)

    return app

def run_local():
    _wait_for_db()
    app = create_app(db)

    app.run(port=3000, server='flask', host='0.0.0.0')


def run_deploy():
    """Run webservice"""
    _wait_for_db()
    app = create_app(db)

    app.run(port=3000, server='gevent', host='0.0.0.0')


def _wait_for_db():
    db.init_engine(
        BASE_DB_URI,
        db_host=CONFIG['app_db_host'],
        db_port=CONFIG['app_db_port'],
        db_name=CONFIG['app_db_name'],
        db_user=CONFIG['app_db_user'],
        db_password=CONFIG['app_db_password'],
        pool_size=CONFIG['app_db_conn_pool_size'])
    db.wait_for_it()


def close_db():
    db.Session.remove()

CONFIG = dict(
    app_db_host='storage',
    app_db_port='5432',
    app_db_name='btracker_db',
    app_db_user='postgres',
    app_db_password='password',
    app_db_conn_pool_size=10,
    environment='test'
)