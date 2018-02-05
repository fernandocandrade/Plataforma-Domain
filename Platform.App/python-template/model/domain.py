from database import Base
from uuid import uuid4
from core.mapper import TemporalMixin, effective_now
import sqlalchemy.dialects.postgresql as sap
from sqlalchemy import UniqueConstraint, Column, Integer, String, DateTime, create_engine, orm, ForeignKey, event
import datetime

class MigrationHistory(Base):
    name = Column(String(80), unique=True, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
