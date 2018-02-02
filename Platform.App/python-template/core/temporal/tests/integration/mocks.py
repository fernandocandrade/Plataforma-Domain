import pytest
from sqlalchemy import Column, String, Integer,ForeignKey, UniqueConstraint, orm
from sqlalchemy.dialects import postgresql as sap

from core.temporal.utils import effective_now
from core.temporal.models import TemporalModelMixin


Base = pytest.BaseModel


class User(Base, TemporalModelMixin):
    temporal = ('name', 'age', )
    name = Column(String)
    age = Column(Integer)


class UserClock(Base):
    ticks = Column(
        Integer,
        nullable=False,
        default=0)

    effective = Column(
        sap.TSTZRANGE(),
        nullable=False,
        default=effective_now)

    entity_id = Column(
        sap.UUID(as_uuid=True),
        ForeignKey('user.id'),
        nullable=False)

    entity = orm.relationship("User")

    __table_args__ = (
        UniqueConstraint('entity_id', 'effective', name='_user_clock_uix'),
    )


class UserNameHistory(Base):
    clock = Column(ForeignKey(UserClock.id))
    ticks = Column(sap.INT4RANGE())
    value = Column(String)

    clock_id = Column(sap.UUID(as_uuid=True), ForeignKey('userclock.id'), nullable=False)
    clock = orm.relationship("UserClock")

    entity_id = Column(sap.UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    entity = orm.relationship("User")


class UserAgeHistory(Base):
    clock = Column(ForeignKey(UserClock.id))
    ticks = Column(sap.INT4RANGE())
    value = Column(Integer)

    clock_id = Column(sap.UUID(as_uuid=True), ForeignKey('userclock.id'), nullable=False)
    clock = orm.relationship("UserClock")

    entity_id = Column(sap.UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    entity = orm.relationship("User")

