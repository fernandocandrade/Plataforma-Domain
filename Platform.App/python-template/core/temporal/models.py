from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects import postgresql

from core.temporal.utils import primary_key, foreign_key, int_range, datetime_range


class TemporalMapper:
    def __call__(self, cls, *args, **kwargs):
        mapper = sa.orm.mapper(cls, *args, **kwargs)
        self.build_clock(cls, mapper.local_table)
        self.build_fields_histories(cls, mapper.local_table)
        return mapper


    def build_fields_histories(self, cls, table):
        if not hasattr(cls, '_history'):
            setattr(cls, '_history', dict())

        for field in cls.Temporal.fields:
            if field in cls._history:
                continue

            history_table_name = f'{cls.__name__}{field}history'
            clock_name = f'{cls._clock.__name__}'
            field_type = getattr(cls, field).property.columns[0].type

            cls._history[field] = type(history_table_name, (cls.__bases__[0], ),{
                "id": primary_key(),
                "ticks": int_range(lower=1),
                "value": sa.Column(field_type, nullable=False),
                "entity_id": foreign_key(table.name),
                "entity": sa.orm.relationship(cls.__name__),
                "clock_id": foreign_key(clock_name),
                "clock": sa.orm.relationship(clock_name)
            })

    def build_clock(self, cls, table):
        if not hasattr(cls, '_clock'):
            setattr(cls, '_clock', dict())

        clock_table_name = f'{cls.__name__}Clock'
        cls._clock = type(clock_table_name, (cls.__bases__[0],), {
            "id": primary_key(),
            "ticks": sa.Column(sa.Integer, default=0),
            "effective": datetime_range(),
            "entity_id": foreign_key(table.name),
            "entity": sa.orm.relationship(cls.__name__),
        })


class TemporalModelMixin:
    @declared_attr
    def __mapper_cls__(cls):
        return TemporalMapper()
