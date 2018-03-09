import itertools
from collections import defaultdict


temporals = {}


def is_temporal(entity):
    if entity not in temporals:
        temporals[entity.__class__] = hasattr(entity, 'Temporal')
    return temporals[entity.__class__]


def temporals_from(collection):
    yield from [item for item in collection if is_temporal(item)]


def before_flush(session, flush_context, instances):
    """This method is intended to listen 'before_flush'
       event from a SQL Alchemy session.
    """
    temporal_structures = []

    for entity in temporals_from(session.deleted):
        clock, clock_created = session.get_or_create_clock(entity)
        clock.deleted = True
        session.expunge(entity)

        if clock_created:
            temporal_structures.append(clock)

    for entity in temporals_from(itertools.chain(session.new, session.dirty)):
        clock, _ = session.get_or_create_clock(entity)
        current_ticks = clock.ticks
        entity_changed = False

        for field in entity.Temporal.fields:
            history, history_created = session.get_or_create_field_history(
                entity, field, clock)

            if history_created:
                temporal_structures.append(history)

                if not entity_changed:
                    entity_changed = True
                    current_ticks += 1

        clock.ticks = current_ticks
        temporal_structures.append(clock)

    session.add_all(temporal_structures)
