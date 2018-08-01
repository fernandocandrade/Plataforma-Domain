from database import Base
from uuid import uuid4
from core.temporal.models import TemporalModelMixin
import sqlalchemy.dialects.postgresql as sap
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import UniqueConstraint, Column, Integer, String, DateTime, create_engine, orm, ForeignKey, event
from datetime import datetime



def get_db_name():
    return "domain"


class conta(Base, TemporalModelMixin):
    def __init__(self, rid=None, _id=None, deleted=False, meta_instance_id=None,
                 titular=None, saldo=None, _metadata=None, branch='master',
                 from_id=None, **kwargs):
        self.rid = rid
        self.id = _id
        self.deleted = deleted
        self.titular = titular
        self.saldo = saldo
        self._metadata = _metadata
        self.meta_instance_id = meta_instance_id
        self.branch = branch
        self.from_id = from_id
        self.modified = kwargs.get('modified',datetime.utcnow())
        self.created_at = kwargs.get('modified',datetime.utcnow())

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
        fields = ('deleted', 'titular', 'saldo', 'meta_instance_id', 'modified', 'created_at', 'from_id', 'branch' )

    titular = Column(String)
    saldo = Column(Integer)

    id = Column(sap.UUID(as_uuid=True), default=uuid4)
    deleted = Column(sap.BOOLEAN())
    meta_instance_id = Column(sap.UUID(as_uuid=True))
    modified = Column(DateTime(), default=datetime.utcnow())
    created_at = Column(DateTime(), default=datetime.utcnow())
    branch = Column(String, default='master')
    from_id = Column(sap.UUID(as_uuid=True))
