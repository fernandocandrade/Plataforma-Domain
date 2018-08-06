import logging
from uuid import uuid4

from sqlalchemy import create_engine, Column
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import database_exists, create_database, drop_database
from settings.loader import Loader
from core.temporal.session import sessionmaker
import log

logging.getLogger('sqlalchemy.engine').setLevel(logging.FATAL)
logging.getLogger('sqlalchemy.dialects').setLevel(logging.FATAL)
logging.getLogger('sqlalchemy.pool').setLevel(logging.FATAL)
logging.getLogger('sqlalchemy.orm').setLevel(logging.FATAL)


conf = Loader().load()
db_host = conf["database"]["host"]
db_name = conf["app"]["name"]
#db_name = domain.get_db_name()
log.info(db_name)
db_user = conf["database"]["user"]
conn_string = f'postgresql+psycopg2://{db_user}@{db_host}:5432/{db_name}'

engine = create_engine(conn_string, convert_unicode=True, isolation_level="READ_UNCOMMITTED",pool_size=20, max_overflow=0)
session_factory = sessionmaker(bind=engine)
db_session = scoped_session(session_factory)


def create_db():
    from model import domain

    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)


def create_session():
    return scoped_session(session_factory)()


class ModelBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    rid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


Base = declarative_base(cls=ModelBase)
Base.query = db_session.query_property()
