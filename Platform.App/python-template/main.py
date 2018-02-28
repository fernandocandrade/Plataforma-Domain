''' Main Module starts all domain app components '''
from migration.sync import sync_db, wait_postgres
if wait_postgres():
    sync_db()

