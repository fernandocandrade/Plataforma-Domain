import psycopg2
import logging as log
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from settings.loader import Loader
env = Loader().load()


def sync_db(db, db_name):
    if should_create_database(db_name):
        create_database(db_name)
        log.debug("created database")
        db.create_all()
        log.debug("database synchronized")
    else:
        migrate(db_name)


def create_database(db_name):
    con = psycopg2.connect(host=env["database"]["host"], database="postgres",
                           user=env["database"]["user"], password=env["database"]["password"])
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    sql = f'create database "{db_name}"'
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


def migrate(db_name):
    print("migrating")
