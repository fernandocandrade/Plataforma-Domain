import itertools

from sqlalchemy import event
from psycopg2 import extras as pg_extras

from core.temporal.utils import effective_now


session = None


def get_or_create_clock_entity(entity, period=effective_now()):
    """Tries to retrieve an entity clock for the given period
       from the database. If it does not exist, a new clock is
       created.
    """
    clock_cls = entity._clock

    clock_entity = session.query(clock_cls)\
        .filter(
            clock_cls.effective.contains(period),
            clock_cls.entity_id == entity.rid
        ).one_or_none()

    if not clock_entity:
        clock_entity = clock_cls()
        clock_entity.effective = period
        clock_entity.entity = entity
        clock_entity.ticks = 0
        session.add(clock_entity)

    return clock_entity


def get_or_create_entity_history(entity, field, clock):
    """Gets an existing or creates a new entity history model
       for an entity temporal field.
    """
    new_value = getattr(entity, field)
    history_cls = entity._history[field]

    history_entity = session.query(history_cls).filter(
        history_cls.entity_id == entity.rid,
        history_cls.clock_id == clock.rid,
        history_cls.ticks.contains(clock.ticks),
    ).one_or_none()

    if not new_value:
        return history_entity, False
    if history_entity:
        if history_entity.value == new_value:
            return history_entity, False

        history_entity.ticks = pg_extras.NumericRange(
            history_entity.ticks.lower, clock.ticks, '[]')

    new_history_entity = history_cls()
    new_history_entity.entity = entity
    new_history_entity.clock = clock
    new_history_entity.ticks = pg_extras.NumericRange(clock.ticks+1)
    new_history_entity.value = new_value
    session.add(new_history_entity)
    return new_history_entity, True


def listen_before_flush(session, flush_context, instances):
    """This method is intended to listen the 'before_flush'
       event from a SQL Alchemy session.
    """
    for entity in itertools.chain(session.new, session.dirty):
        if not hasattr(entity, 'Temporal'):
            continue

        clock = get_or_create_clock_entity(entity)
        current_ticks = clock.ticks
        entity_changed = False

        for col in entity.Temporal.fields:
            entity_history, created_history = get_or_create_entity_history(
                entity, col, clock)

            if not entity_changed and created_history:
                entity_changed = True
                current_ticks += 1

        clock.ticks = current_ticks


def init_temporal_session(s):
    """Inits a temporal session on an existing SQL Alchemy session.
    """
    global session
    session = s

    if hasattr(session, '_temporal'):
        return

    setattr(session, '_temporal', True)
    event.listen(s, 'before_flush', listen_before_flush)
