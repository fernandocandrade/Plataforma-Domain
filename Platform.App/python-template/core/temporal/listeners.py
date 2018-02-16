import itertools


def before_flush(session, flush_context, instances):
    """This method is intended to listen 'before_flush'
       event from a SQL Alchemy session.
    """
    for entity in itertools.chain(session.new, session.dirty):
        if not hasattr(entity, 'Temporal'):
            continue

        clock, _ = session.get_or_create_clock(entity)
        current_ticks = clock.ticks
        entity_changed = False

        for field in entity.Temporal.fields:
            _, history_created = session.get_or_create_field_history(
                entity, field, clock)

            if not entity_changed and history_created:
                entity_changed = True
                current_ticks += 1

        clock.ticks = current_ticks
