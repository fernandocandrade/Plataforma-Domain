from database import Base
from uuid import uuid4
from core.temporal.models import TemporalModelMixin
import sqlalchemy.dialects.postgresql as sap
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import UniqueConstraint, Column, Integer, String, DateTime, create_engine, orm, ForeignKey, event
import datetime

class MigrationHistory(Base):
    def __init__(self, name, created_date=None):
        self.name = name
        self.created_date = created_date

    name = Column(String(80), unique=True, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

def get_db_name():
    return "domain"


class Conta(Base, TemporalModelMixin):

    def __init__(self, titular=None,saldo=None, _metadata=None, **kwargs):
        self.titular = titular
        self.saldo = saldo
        self._metadata = _metadata

    def dict(self):
        return {
            "titular": self.titular,"saldo": self.saldo,
            "id": self.id,
            "_metadata": self._metadata
        }

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    class Temporal:
        fields = ('titular','saldo', )

    titular = Column(String)
    saldo = Column(Integer)

    id = Column(sap.UUID(as_uuid=True), primary_key=True, default=uuid4)
