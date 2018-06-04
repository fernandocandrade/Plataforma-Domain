from model.persistence import Persistence
from model.domain import *
from sdk import process_memory, event_manager, process_instance, domain_dependency
from mapper.builder import MapBuilder
from dateutil import parser
from datetime import datetime
import pytz
import log
from uuid import uuid4
import copy
import hashlib
import json
from utils.pruu import log_on_pruu
import log

class ReprocessingManager:

    def __init__(self, process_id=None, instance_id=None):
        self.process_id = process_id
        self.instance_id = instance_id

    def dispatch_reprocessing_events(self, items):
        log.info("Dispatching reprocessing events")
        events_to_execute = self.get_reprocessing_events(items)
        reprocessing_document = self.get_reprocessing_document(events_to_execute)
        if len(reprocessing_document["events"]) == 0:
            return
        if  not process_memory.save_document("reprocessing",reprocessing_document):
            """TODO qual a melhor maneira de tratar esse caso de falha?
                talvez enviar para uma fila no rabbit?
            """
            log.critical("cannot save reprocessing documento on process memory")
            log.critical(reprocessing_document)
            log.critical("Reprocessing aborted!")
            event_manager.push({"name":"system.reprocessing.error", "payload":{"message":"Reprocessing was aborted due process memory saved reprocessing document", "document":reprocessing_document}})
        else:
            for event in reprocessing_document["events"]:
                event_manager.push(event)

    def get_reprocessing_document(self, events):
        reprocessing_document = {}
        reprocessing_document["events"] = []
        for event in events:
            reprocessing_document["id"] = event["reprocessing"]["id"]
            reprocessing_document["events"].append(event)
            log.info(f"Need to re-execute {event['name']} from process {event['reprocessing']['app_name']} instance {event['reprocessing']['process_id']} branch {event['branch']}")
            event["scope"] = "reprocessing"
        return reprocessing_document

    def get_reprocessing_events(self, items):
        processes = self.get_impacted_processes(items)
        events_to_execute = self.get_events_to_execute(processes)
        events_to_execute = self.group_events(events_to_execute)
        if len(events_to_execute) > 0:
            log.info(f"Reprocessing {len(events_to_execute)} events")
        return events_to_execute

    def get_events_to_execute(self, processes):
        events_to_execute = []
        reprocessing_id = str(uuid4())
        for p in processes:
            head = process_memory.head(p["id"])
            event_to_reprocess = head["event"]
            event_to_reprocess["reprocessing"] = {}
            event_to_reprocess["reprocessing"]["id"] = reprocessing_id
            event_to_reprocess["reprocessing"]["event_tag"] = str(uuid4())
            event_to_reprocess["reprocessing"]["executed_at"] = p["startExecution"]
            event_to_reprocess["reprocessing"]["instance_id"] = p["id"]
            event_to_reprocess["reprocessing"]["app_name"]    = p["appName"]
            event_to_reprocess["reprocessing"]["process_id"]  = p["processId"]
            event_to_reprocess["reprocessing"]["system_id"]   = p["systemId"]
            event_to_reprocess["reprocessing"]["version"]     = p["version"]
            event_to_reprocess["reprocessing"]["event_out"]   = head["eventOut"]
            event_to_reprocess["reprocessing"]["executed"]    = False
            event_to_reprocess["reprocessing"]["payload_signature"] = hashlib.sha1(str(json.dumps(event_to_reprocess["payload"], sort_keys=True)).encode("utf-8")).hexdigest()
            events_to_execute.append(event_to_reprocess)
        return events_to_execute


    def group_events(self, events):
        exist = set()
        result = []
        for event in events:
            if event["branch"] != "master":
                continue
            reprocessing = event["reprocessing"]
            key = f"{reprocessing['process_id']}:{reprocessing['version']}:{reprocessing['payload_signature']}:{event['branch']}"
            if not key in exist:
                exist.add(key)
                result.append(event)
        return result

    def get_impacted_processes(self, items):
        older_data = pytz.UTC.localize(datetime.utcnow())
        impacted_domain = set()
        current_branch = "master"
        for item in items:
            current_branch = item.branch
            date = pytz.UTC.localize(item.modified)
            log.info(f"{date} < {older_data}")
            if date < older_data:
                older_data = date
            impacted_domain.add(type(item).__name__)

        log.info(f"Older data at {older_data}")
        instances =  process_instance.ProcessInstance().get_processes_after(older_data, self.instance_id, self.process_id)
        deps = []
        for instance in instances:
            result = domain_dependency.DomainDependency().get_dependency_by_process_and_version(instance["processId"],instance["version"], impacted_domain)
            if len(result) > 0:
                instance["appName"] = result[0]["name"]
                instance["branch"] = current_branch
                deps.append(instance)
        return deps

