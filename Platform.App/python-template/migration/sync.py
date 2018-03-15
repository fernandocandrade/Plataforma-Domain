import psycopg2
import log
from alembic.operations import Operations
import sqlalchemy as sa
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from settings.loader import Loader
from database import db_name, Base, engine
import glob
import yaml
from uuid import uuid4
import datetime
import time

env = Loader().load()


def wait_postgres():
    total = 10
    count = 1
    while count <= total:
        try:
            con = psycopg2.connect(host=env["database"]["host"], database="postgres",
                            user=env["database"]["user"], password=env["database"]["password"])
            con.close()
            return True
        except Exception as ex:
            log.info(str(ex))
            log.info(f"host: {env['database']['host']}")
            log.info(f"cannot connect to postgres retry: {count} left: {total - count}")
            time.sleep(5)
            count += 1

    log.info(f"cannot connect to postgres after {total} retries")
    return False

