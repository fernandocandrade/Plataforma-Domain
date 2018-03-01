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


def sync_db(name=db_name):
    if should_create_database(name):
        create_database(name)
        log.info("created database")
    Base.metadata.create_all(bind=engine)
    log.info("database synchronized")


def wait_postgres():
    total = 10
    count = 1
    if should_create_database(env["database"]["name"]):
        create_database(env["database"]["name"])
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


def create_database(db_name):
    con = psycopg2.connect(host=env["database"]["host"], database="postgres",
                           user=env["database"]["user"], password=env["database"]["password"])
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    sql = f'create database "{db_name}"'
    cur.execute(sql)
    con.close()

def drop_database(db_name):
    if db_name == "postgres":
        return
    con = psycopg2.connect(host=env["database"]["host"], database="postgres",
                           user=env["database"]["user"], password=env["database"]["password"])
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    sql = f'drop database "{db_name}"'
    cur.execute(sql)
    con.close()

def raw_sql(db_name, sql):
    con = psycopg2.connect(host=env["database"]["host"], database=db_name,
                           user=env["database"]["user"], password=env["database"]["password"])
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute(sql)
    recset = cur.fetchall()
    con.close()
    return recset

def raw_execute(db_name, sql):
    con = psycopg2.connect(host=env["database"]["host"], database=db_name,
                           user=env["database"]["user"], password=env["database"]["password"])
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute(sql)
    con.close()


def should_create_database(db_name):
    con = psycopg2.connect(host=env["database"]["host"], database="postgres",
                           user=env["database"]["user"], password=env["database"]["password"])
    cur = con.cursor()
    cur.execute(
        f"SELECT datname FROM pg_database where datname='{db_name}'")
    recset = cur.fetchall()
    result = []
    for rec in recset:
        result.append(rec)
    con.close()
    return not result




