''' Main Module starts all domain app components '''
from migration.sync import wait_postgres
from database import create_db


if wait_postgres():
    create_db()
