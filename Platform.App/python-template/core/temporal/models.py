from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.dialects import postgresql

from core.temporal.utils import effective_now


class TemporalModelMixin:
    temporal = tuple()
    history = dict()
    _clock = None

    @classmethod
    def build_field_history_table(cls, table):
        for field in cls.temporal:
            history_table = type(f"{cls.__name__}{field}history", (cls.__bases__[0], ), {
                "id": sa.Column(
                    postgresql.UUID(as_uuid=True),
                    primary_key=True,
                    default=uuid4),
                "ticks": sa.Column(
                    postgresql.INT4RANGE(),
                    nullable=False,
                    default='[1,]'),
                "value": sa.Column(
                    sa.String,
                    nullable=False,
                    default='[1,]'),
                "entity_id": sa.Column(
                    postgresql.UUID(as_uuid=True),
                    sa.ForeignKey(f'{table.name}.id'),
                    nullable=False
                ),
                "clock_id": sa.Column(
                    postgresql.UUID(as_uuid=True),
                    sa.ForeignKey(f'{table.name}clock.id'),
                    nullable=False
                ),
                "entity": sa.orm.relationship(cls.__name__),
                "clock": sa.orm.relationship(f'{cls.__name__}Clock')
            })

            cls.history.setdefault(field, history_table)

    @classmethod
    def build_clock(cls, mapper):
        table = mapper.local_table
        clock_table = type(f"{cls.__name__}Clock", (cls.__bases__[0],), {
            "id": sa.Column(
                    postgresql.UUID(as_uuid=True),
                    primary_key=True,
                    default=uuid4),
            "ticks": sa.Column(
                    sa.Integer,
                    default=0),
            "effective": sa.Column(
                    postgresql.TSTZRANGE(),
                    nullable=False,
                    default=effective_now),
            "entity_id": sa.Column(
                    postgresql.UUID(as_uuid=True),
                    sa.ForeignKey(f'{table.name}.id'),
                    nullable=False
            ),
            "entity": sa.orm.relationship(cls.__name__),
        })

        cls._clock = clock_table

    @declared_attr
    def __mapper_cls__(cls):
        def mapper(cls_, *args, **kwargs):
            _mapper = sa.orm.mapper(cls_, *args, **kwargs)
            cls.build_clock(_mapper)
            cls.build_field_history_table(_mapper.local_table)
            return _mapper
        return mapper
