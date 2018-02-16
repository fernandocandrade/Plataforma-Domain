import logging

logging.getLogger('sqlalchemy.engine').setLevel(logging.FATAL)
logging.getLogger('sqlalchemy.dialects').setLevel(logging.FATAL)
logging.getLogger('sqlalchemy.pool').setLevel(logging.FATAL)
logging.getLogger('sqlalchemy.orm').setLevel(logging.FATAL)

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
import sqlalchemy.dialects.postgresql as sap
from uuid import uuid4
from settings.loader import Loader
from sqlalchemy import UniqueConstraint, Column, Integer, String, DateTime, create_engine, orm, ForeignKey, event
from core.temporal.session import sessionmaker

conf = Loader().load()
db_host = conf["database"]["host"]
db_name = conf["app"]["name"]
db_user = conf["database"]["user"]
conn_string = f'postgresql+psycopg2://{db_user}@{db_host}:5432/{db_name}'

engine = create_engine(conn_string, convert_unicode=True, )
session_factory = sessionmaker(bind=engine)
db_session = scoped_session(session_factory)



def create_session():
    session = scoped_session(session_factory)()
    return session


class ModelBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(sap.UUID(as_uuid=True), primary_key=True, default=uuid4)

    def save(self):
        self.objects.save(self)

Base = declarative_base(cls=ModelBase)

Base.query = db_session.query_property()

import model.domain
