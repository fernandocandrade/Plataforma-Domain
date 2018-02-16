import datetime as dt
from uuid import uuid4
import itertools
from sqlalchemy import Column, Integer, String, DateTime, create_engine, orm, ForeignKey, event, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from psycopg2 import extras as psql_extras
import sqlalchemy.dialects.postgresql as sap


engine = create_engine(
    'postgresql+psycopg2://postgres@127.0.0.1:5432/postgres',
    echo=False)
sessionmaker = orm.sessionmaker(bind=engine)
session = sessionmaker()


class ModelBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(sap.UUID(as_uuid=True), primary_key=True, default=uuid4)

    def save(self):
        self.objects.save(self)


Base = declarative_base(cls=ModelBase)


class UserData:
    @staticmethod
    def save(obj):
        session.add(obj)

    @staticmethod
    def count():
        return session.query(User).count()


def effective_now() -> psql_extras.DateTimeTZRange:
    utc_now = dt.datetime.now(tz=dt.timezone.utc)
    return psql_extras.DateTimeTZRange(utc_now, None)


class TemporalMixin:
    @classmethod
    def get_classname(cls):
        return cls.__name__

    @classmethod
    def get_clock_name(cls):
        return f"{cls.get_classname()}Clock"

    @classmethod
    def get_history_name(cls, field):
        return f"{cls.get_classname()}{field.title()}History"




class User(Base, TemporalMixin):
    temporal = ('name', )
    name = Column(String)


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


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


def get_or_create_clock_entity(self, period=effective_now()):
    """Tries to retrieve an entity clock for the given period
       from the database. If it does not exist, a new clock is
       created.
    """
    clock_cls = globals()[self.get_clock_name()]

    clock_entity = session.query(clock_cls)\
        .filter(clock_cls.effective.contains(period), clock_cls.entity_id == self.id)\
        .one_or_none()

    if not clock_entity:
        clock_entity = clock_cls()
        clock_entity.effective = period
        clock_entity.entity = self
        clock_entity.ticks = 0
        session.add(clock_entity)

    return clock_entity


def get_or_create_entity_history(self, field, clock):
    new_value = getattr(self, field)
    history_cls = globals()[self.get_history_name(field)]

    history_entity = session.query(history_cls)\
        .filter(
            history_cls.entity_id == self.id,
            history_cls.clock_id == clock.id,
            history_cls.ticks.contains(clock.ticks),
        ).one_or_none()

    if history_entity:
        if history_cls.value == new_value:
            return history_entity, False

        history_entity.ticks = f'[{history_entity.ticks.lower}, {clock.ticks}]'

    new_history_entity = history_cls()
    new_history_entity.entity = self
    new_history_entity.clock = clock
    new_history_entity.ticks = f'[{clock.ticks + 1},]'
    new_history_entity.value = new_value
    session.add(new_history_entity)
    return new_history_entity, True


@event.listens_for(session, 'before_flush')
def receive_before_flush(session, flush_context, instances):
    for entity in itertools.chain(session.new, session.dirty):
        if not entity.temporal:
            continue

        clock = get_or_create_clock_entity(entity)
        changed = False

        for col in entity.temporal:
            entity_history, created = get_or_create_entity_history(
                entity, col, clock)

            if not changed and created:
                changed = True
                clock.ticks += 1
