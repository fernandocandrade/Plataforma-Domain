''' Main Module starts all domain app components '''
from migration.sync import sync_db
from api.server import app
import log

log.info("starting app")
sync_db()
log.info("starting api server")
app.run()