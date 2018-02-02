''' Main Module starts all domain app components '''
from migration.sync import sync_db
from cross_cutting import db, app, get_db_name

sync_db(db, get_db_name())
app.run()