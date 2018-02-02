import datetime
from psycopg2 import extras as pg_extras


def effective_now():
    """UTC open datetime range starting from now.
    """
    utc_now = datetime.datetime.now(tz=datetime.timezone.utc)
    return pg_extras.DateTimeTZRange(utc_now, None)
