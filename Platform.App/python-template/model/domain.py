from database import Base
from uuid import uuid4
from core.temporal.models import TemporalModelMixin
import sqlalchemy.dialects.postgresql as sap
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import UniqueConstraint, Column, Integer, String, DateTime, create_engine, orm, ForeignKey, event
import datetime



def get_db_name():
    return "domain"


class conta(Base, TemporalModelMixin):

    def __init__(self, id=None, meta_instance_id=None , titular=None,saldo=None, _metadata=None, **kwargs):
        self.id = id
        self.titular = titular
        self.saldo = saldo
        self._metadata = _metadata
        self.meta_instance_id = meta_instance_id

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
        fields = ('titular','saldo', 'meta_instance_id', )

    titular = Column(String)
    saldo = Column(Integer)

    id = Column(sap.UUID(as_uuid=True), primary_key=True, default=uuid4)
    meta_instance_id = Column(sap.UUID(as_uuid=True))
