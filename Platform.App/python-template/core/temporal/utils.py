from uuid import uuid4
from datetime import datetime, timezone

from psycopg2 import extras as pg_extras
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def effective_now():
    """UTC DateTime Range starting from now.
    """
    utc_now = datetime.now(tz=timezone.utc)
    return pg_extras.DateTimeTZRange(utc_now, None)


def primary_key():
    """Primary Key UUID column mapping.
    """
    return sa.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid4)


def datetime_range(lower=datetime.now(tz=timezone.utc),
                   upper=None, nullable=False):
    """Postgres DateTime Range column mapping.
    """
    return sa.Column(
        postgresql.TSTZRANGE(),
        default=pg_extras.DateTimeTZRange(lower, upper),
        nullable=nullable)


def int_range(lower=0, upper=None, nullable=False):
    """Postgres Int4Range column mapping.
    """
    return sa.Column(
        postgresql.INT4RANGE(),
        default=pg_extras.NumericRange(lower, upper),
        nullable=nullable)


def foreign_key(target_table, nullable=False):
    """ForeignKey Column mapping.
    """
    return sa.Column(
        postgresql.UUID(as_uuid=True),
        sa.ForeignKey(f'{target_table.lower()}.id'),
        nullable=nullable)
