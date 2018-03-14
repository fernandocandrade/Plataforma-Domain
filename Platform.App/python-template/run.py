import os
instance_id = os.environ.get("INSTANCE_ID", "undefined")
from model.persistence import Persistence
from mapper.builder import MapBuilder
from database import create_db, create_session
from model.batch import BatchPersistence
import log
create_db()
log.info("Executing batch persist")
session = create_session()
try:
    batch = BatchPersistence(session)
    batch.run(instance_id)
except Exception as ex:
    log.critical(str(ex))
    session.rollback()
finally:
    session.close()
log.info("Batch persist executed with success")

