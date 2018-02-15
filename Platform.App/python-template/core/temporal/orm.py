from datetime import datetime

from sqlalchemy import orm

from core.temporal.utils import effective_now


class TemporalQuery(orm.Query):
    def clock(self, entity, period=effective_now()):
        cls = entity._clock

        return self.session.query(cls).filter(
            cls.effective.contains(period),
            cls.entity_id == entity.id
        ).one_or_none()

    def field_history(self, entity, field, clock):
        cls = entity._history[field]

        return self.session.query(cls).filter(
            cls.entity_id == entity.id,
            cls.clock_id == clock.id,
            cls.ticks.contains(clock.ticks),
        ).one_or_none()

    def history(self, period=datetime.utcnow(), version=None, fields=None):
        cls = self.column_descriptions[0]['entity']

        if not hasattr(cls, 'Temporal'):
            raise Exception("not temporal")

        query = self.options(orm.load_only('id'))\
            .join((cls._clock, cls.id == cls._clock.entity_id))\
            .filter(cls._clock.effective.contains(period))

        for field in fields if fields else cls.Temporal.fields:
            history = cls._history[field]
            query = query\
                .add_column(history.value.label(field))\
                .join(history, cls.id == history.entity_id)

            if version:
                query = query.filter(
                    history.ticks.contains(version))

        return query
