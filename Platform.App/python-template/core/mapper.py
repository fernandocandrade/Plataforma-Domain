import datetime as dt
from uuid import uuid4
from sqlalchemy import Column, Integer, String, DateTime, create_engine, orm, ForeignKey, event
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from psycopg2 import extras as psql_extras
import sqlalchemy.dialects.postgresql as sap


engine = create_engine(
    'postgresql+psycopg2://postgres@127.0.0.1:5432/postgres',
    echo=True)
sessionmaker = orm.sessionmaker(bind=engine)
session = sessionmaker()


class ModelBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(sap.UUID(as_uuid=True), primary_key=True, default=uuid4())

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

    def get_entity_history(self, field, clock):
        history_instance = globals()[self.get_history_name(field)]()
        history_instance.value = getattr(self, field)
        history_instance.entity = self
        history_instance.ticks = '[1,]'
        history_instance.clock = clock
        clock.entity = self
        return history_instance

    def get_clock_entity(cls):
        clock_entity = globals()[cls.get_clock_name()]()
        clock_entity.effective = effective_now()
        return clock_entity



class User(Base, TemporalMixin):
    objects = UserData
    temporal = ('name', )
    name = Column(String)


class UserClock(Base):
    ticks = Column(sap.INT4RANGE(), nullable=False, default='[1,)')
    effective = Column(sap.TSTZRANGE(), nullable=False, default=effective_now)

    entity_id = Column(sap.UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    entity = orm.relationship("User")

class UserNameHistory(Base):
    clock = Column(ForeignKey(UserClock.id))
    ticks = Column(sap.INT4RANGE())
    value = Column(String)

    clock_id = Column(sap.UUID(as_uuid=True), ForeignKey('userclock.id'), nullable=False)
    clock = orm.relationship("UserClock")

    entity_id = Column(sap.UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    entity = orm.relationship("User")


Base.metadata.create_all(engine)


@event.listens_for(session, 'before_flush')
def receive_before_flush(session, flush_context, instances):
    for entity in session.new:
        clock_entity = entity.get_clock_entity()
        session.add(clock_entity)

        for col in entity.temporal:
            entity_history = entity.get_entity_history(col, clock_entity)
            session.add(entity_history)


