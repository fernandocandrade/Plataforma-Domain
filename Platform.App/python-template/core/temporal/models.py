from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects import postgresql

from core.temporal.utils import primary_key, foreign_key, int_range, datetime_range


class TemporalModelMixin:
    temporal = tuple()
    _history = dict()
    _clock = None

    @classmethod
    def build_field_history_table(cls, table):
        for field in cls.Temporal.fields:
            if field in cls._history:
                continue

            history_table_name = f"{cls.__name__}{field}history"
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

    @classmethod
    def build_clock(cls, mapper):
        table = mapper.local_table
        clock_table_name = f"{cls.__name__}Clock"
        cls._clock = type(clock_table_name, (cls.__bases__[0],), {
            "id": primary_key(),
            "ticks": sa.Column(sa.Integer, default=0),
            "effective": datetime_range(),
            "entity_id": foreign_key(table.name),
            "entity": sa.orm.relationship(cls.__name__),
        })

    @declared_attr
    def __mapper_cls__(cls):
        def mapper(cls_, *args, **kwargs):
            _mapper = sa.orm.mapper(cls_, *args, **kwargs)
            cls.build_clock(_mapper)
            cls.build_field_history_table(_mapper.local_table)
            return _mapper
        return mapper
