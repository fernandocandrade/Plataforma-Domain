from sqlalchemy import event, orm
from psycopg2 import extras as pg_extras

from core.temporal.orm import TemporalQuery
from core.temporal.listeners import before_flush
from core.temporal.utils import effective_now


class TemporalSession(orm.session.Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.temporal_deleted = []

    def create_clock(self, entity, period=effective_now()):
        """creates a new clock for a temporal model.
        """
        clock = entity._clock()
        clock.effective = period
        clock.entity = entity
        clock.ticks = 0
        #  self.add(clock)
        return clock

    def get_or_create_clock(self, entity, period=effective_now()):
        """gets an existing or creates a new entity clock
           for a temporal model.
        """
        if entity.rid:
            clock = self.query(entity.__class__).clock(entity, period)

            if clock:
                return clock, False

        return self.create_clock(entity, period), True

    def create_field_history(self, entity, field, clock, value):
        """creates a new entity field history.
        """
        history = entity._history[field]()
        history.entity = entity
        history.clock = clock
        history.ticks = pg_extras.NumericRange(clock.ticks+1)
        history.value = value
        #  self.add(history)
        return history

    def get_or_create_field_history(self, entity, field, clock):
        """gets an existing or creates a new entity history field
           for a temporal model.
        """
        new_value = getattr(entity, field)

        #if not new_value:
        #    return None, False

        if entity.rid:
            history = self.query(entity.__class__).field_history(
                entity, field, clock)

            if history:
                if history.value == new_value:
                    return history, False

                history.ticks = pg_extras.NumericRange(
                    history.ticks.lower, clock.ticks, '[]')

        new_history = self.create_field_history(
            entity, field, clock, new_value)

        return new_history, True


def _init_temporal_session(session):
    """Inits a temporal session on an existing SQL Alchemy session.
    """
    if hasattr(session, '_temporal'):
        return

    setattr(session, '_temporal', True)
    event.listen(session, 'before_flush', before_flush)


class sessionmaker(orm.sessionmaker):
    """temporal session factory."""
    def __init__(self, *args, **kwargs):
        super().__init__(class_=TemporalSession, *args, **kwargs)

    def __call__(self, **kwargs):
        session = super().__call__(query_cls=TemporalQuery, **kwargs)
        _init_temporal_session(session)
        return session

