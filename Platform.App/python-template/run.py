import os
from model.persistence import Persistence
from database import create_db, create_session
from model.batch import BatchPersistence
from merge import MergeBranch
import log

instance_id = os.environ.get("INSTANCE_ID", "undefined")
solution_id = os.environ.get("SYSTEM_ID")
event = os.environ.get('EVENT')

create_db()
log.info("Executing batch persist")
session = create_session()


strategies = {
    f'{solution_id}.persist.request': BatchPersistence,
    f'{solution_id}.merge.request': MergeBranch,
}


try:
    batch = strategies[event](session)
    batch.run(instance_id, solution_id, event)
    log.info("Batch persist executed with success")
except Exception as ex:
    log.critical(str(ex))
    session.rollback()
finally:
    session.close()
    log.info("Batch persist worker finished")


