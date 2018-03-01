from uuid import uuid4

import pytest
from sqlalchemy import create_engine, orm, Column
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils import database_exists, create_database, drop_database

from core.temporal.session import sessionmaker

from database import Base


class SETTINGS:
    DB_HOST = "127.0.0.1"
    DB_PORT = 5432
    DB_NAME = "app_name"
    DB_USER = "postgres"
    DB_PASSWORD = ""
    KEEP_DB = False


@pytest.fixture(scope='session')
def engine(request):
    """Creates a new database connection for each test section.
    """
    engine = create_engine(
        f'postgresql+psycopg2://{SETTINGS.DB_USER}@{SETTINGS.DB_HOST}:{SETTINGS.DB_PORT}/{SETTINGS.DB_NAME}',
        echo=False)

    if not database_exists(engine.url):
        create_database(engine.url)

    def teardown():
        if not SETTINGS.KEEP_DB:
            drop_database(engine.url)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture(scope='session', autouse=True)
def db(request, engine):
    _db = Base.metadata
    _db.create_all(engine)
    return _db


@pytest.fixture(scope='function')
def session(request, engine):
    """Creates a new temporal session for a test."""
    connection = engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker(bind=connection)
    session = orm.scoped_session(session_factory)

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
