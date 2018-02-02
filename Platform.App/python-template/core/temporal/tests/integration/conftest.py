from uuid import uuid4

import pytest
from sqlalchemy import create_engine, orm, Column
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.dialects import postgresql

from core.temporal.core import init_temporal_session


class SETTINGS:
    DB_HOST = "127.0.0.1"
    DB_PORT = 5432
    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASSWORD = ""


@pytest.fixture(scope='session')
def engine(request):
    """Creates a new database connection for each test section.
    """
    engine = create_engine(
        f'postgresql+psycopg2://{SETTINGS.DB_USER}@{SETTINGS.DB_HOST}:{SETTINGS.DB_PORT}/{SETTINGS.DB_NAME}',
        echo=True)

    pytest.BaseModel.metadata.drop_all(engine)
    pytest.BaseModel.metadata.create_all(engine)
    return engine


@pytest.fixture(scope='function')
def session(request, engine):
    """Creates a database session for each test.
    """
    session = orm.sessionmaker(bind=engine)()
    init_temporal_session(session)
    return session


def pytest_namespace():
    """
    """
    class ModelBase:
        @declared_attr
        def __tablename__(cls):
            return cls.__name__.lower()

        id = Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=uuid4)

    Base = declarative_base(cls=ModelBase)

    return {
        'BaseModel': Base
    }


@pytest.fixture
def create_model(request, session):
    def _create_model(cls, **kwargs):
        model = cls(**kwargs)
        session.add(model)
        session.commit()
        return model
    return _create_model


@pytest.fixture
def update_model(session):
    def _update_model(instance, **kwargs):
        for k,v in kwargs.items():
            setattr(instance, k, v)
        session.commit()
    return _update_model


@pytest.fixture
def query_by_entity(session):
    def _query_by_entity(cls, entity_id, order_by=None):
        query = session.query(cls).filter(cls.entity_id == entity_id)
        if order_by:
            return query.order_by(cls.value)
        return query

    return _query_by_entity
