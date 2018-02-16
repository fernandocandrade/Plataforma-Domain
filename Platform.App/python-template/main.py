''' Main Module starts all domain app components '''
from migration.sync import sync_db
from api.server import app
import log
import logging
logging.basicConfig()

log.info("starting app")
sync_db()
log.info("starting api server")
app.run()