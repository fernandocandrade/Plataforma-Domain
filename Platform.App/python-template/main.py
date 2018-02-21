''' Main Module starts all domain app components '''
from migration.sync import sync_db
from utils.config_loader import load_config_file
from api.server import app
import log
import logging
logging.basicConfig()

log.info("starting app")
sync_db()
log.info("starting api server")
cnf = load_config_file()
log.info(f"Server running on host=0.0.0.0 and port={cnf['http']['port']}")
app.run(host='0.0.0.0', port=cnf["http"]["port"])
