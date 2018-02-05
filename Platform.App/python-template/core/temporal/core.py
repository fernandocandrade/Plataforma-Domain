import itertools

from sqlalchemy import event

from core.temporal.utils import effective_now


session = None


def get_or_create_clock_entity(entity, period=effective_now()):
    """Tries to retrieve an entity clock for the given period
       from the database. If it does not exist, a new clock is
       created.
    """
    clock_cls = entity._clock

    clock_entity = session.query(clock_cls)\
        .filter(clock_cls.effective.contains(period), clock_cls.entity_id == entity.id)\
        .one_or_none()

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
    history_cls = entity.history[field]

    history_entity = session.query(history_cls).filter(
        history_cls.entity_id == entity.id,
        history_cls.clock_id == clock.id,
        history_cls.ticks.contains(clock.ticks),
    ).one_or_none()

    if history_entity:
        if history_cls.value == new_value:
            return history_entity, False

        history_entity.ticks = f'[{history_entity.ticks.lower}, {clock.ticks}]'

    new_history_entity = history_cls()
    new_history_entity.entity = entity
    new_history_entity.clock = clock
    new_history_entity.ticks = f'[{clock.ticks + 1},]'
    new_history_entity.value = new_value
    session.add(new_history_entity)
    return new_history_entity, True


def listen_before_flush(session, flush_context, instances):
    """This method is intended to listen the 'before_flush'
       event from a SQL Alchemy session.
    """
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


def init_temporal_session(s):
    """Inits a temporal session on an existing SQL Alchemy session.
    """
    global session
    session = s
    event.listen(s, 'before_flush', listen_before_flush)
