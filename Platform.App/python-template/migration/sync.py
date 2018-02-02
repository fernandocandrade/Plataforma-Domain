import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from settings.loader import Loader
from model.domain import get_db_name
env = Loader().load()

def sync_db(db):
    if should_create_database():
        create_database(get_db_name())
        db.create_all()
    else:
        migrate(get_db_name())

def create_database(db_name):
    con = psycopg2.connect(host=env["database"]["host"], database="postgres",
    user=env["database"]["user"], password=env["database"]["password"])
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    sql = f'create database "{db_name}"'
    cur.execute(sql)
    con.close()

def should_create_database():
    con = psycopg2.connect(host=env["database"]["host"], database="postgres",
    user=env["database"]["user"], password=env["database"]["password"])
    cur = con.cursor()
    cur.execute(f"SELECT datname FROM pg_database where datname='{get_db_name()}'")
    recset = cur.fetchall()
    result = []
    for rec in recset:
        result.append(rec)
    con.close()
    return not result

def migrate(db_name):
    print("migrating")

