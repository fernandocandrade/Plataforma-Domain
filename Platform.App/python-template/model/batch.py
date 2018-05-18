from model.persistence import Persistence
from model.domain import *
from sdk import process_memory, event_manager, process_instance, domain_dependency
from mapper.builder import MapBuilder
from dateutil import parser
from datetime import datetime
import pytz
import log
import copy
import hashlib
import json
from utils.pruu import log_on_pruu

class BatchPersistence:

    def __init__(self,session):
        self.session = session
        self.process_id = None
        self.instance_id = None

    def get_head_of_process_memory(self, instance_id):
        return process_memory.head(instance_id)

    def extract_head(self, head):
        self.event = head.get("event",{})
        self.instance_id = head.get("instanceId")
        self.process_id = head.get("processId")
        self.system_id = head.get("systemId")
        self.fork = head.get("fork")
        if "map" in head:
            self.map = {
                "map": head["map"].get("content",{}),
                "app_name": head["map"]["name"]
            }
            self.mapper = MapBuilder().build_from_map(self.map)
        else:
            self.map = {}
        if "dataset" in head:
            self.entities = head["dataset"].get("entities",[])
        else:
            self.entities = []
        self.event_out = head.get("eventOut","system.persist.eventout.undefined")

    def get_items_to_persist(self, entities, instance_id):
        """ process head and collect data to persist on domain """
        items = []
        for entity in entities:
            for item in entities[entity]:
                if not self.has_change_track(item):
                    continue
                domain_obj = self.mapper.translator.to_domain(self.map["app_name"], item)
                domain_obj["meta_instance_id"] = instance_id
                domain_obj["branch"] = item["_metadata"].get("branch", "master")
                items.append(domain_obj)
        return items


    def has_change_track(self, item):
        return "_metadata" in item and "changeTrack" in item['_metadata']


    def run(self, instance_id):
        try:
            log.info(f"getting data from process memory with instance id {instance_id}")
            head = self.get_head_of_process_memory(instance_id)
            log.info("extracting data from dataset")
            self.extract_head(head)
            log.info("getting items to persist")
            items = self.get_items_to_persist(self.entities, instance_id)
            log.info(f"should persist {len(items)} objects in database")
            instances = self.persist(items)
            log.info("objects persisted")
            parts = self.event["name"].split(".")
            parts.pop()
            parts.append("done")
            name = ".".join(parts)
            log.info(f"pushing event {name} to event manager")
            evt = {"name":self.event_out, "instanceId":instance_id, "scope":self.event["scope"], "branch": self.event["branch"] , "payload":{"instance_id":instance_id}}
            event_manager.push(evt)
            self.dispatch_reprocessing_events(instances, self.instance_id, self.process_id)

        except Exception as e:
            event_manager.push({"name":"system.process.persist.error", "instanceId":instance_id, "payload":{"instance_id":instance_id, "origin":self.event}})
            log.info("exception occurred")
            log.critical(e)
            raise e

    def dispatch_reprocessing_events(self, items, instance_id, process_id):
        log.info("Dispatching reprocessing events")
        self.instance_id = instance_id
        self.process_id = process_id
        processes = self.get_impacted_processes(items)


        events_to_execute = self.get_events_to_execute(processes)
        events_to_execute = self.group_events(events_to_execute)
        if len(events_to_execute) > 0:
            log.info(f"Reprocessing {len(events_to_execute)} events")
        for event in events_to_execute:
            log.info(f"Need to re-execute {event['name']} from process {event['reprocessing']['app_name']} instance {event['reprocessing']['process_id']} branch {event['branch']}")
            event["scope"] = "reprocessing"
            event_manager.push(event)

    def get_events_to_execute(self, processes):
        events_to_execute = []
        for p in processes:
            head = self.get_head_of_process_memory(p["id"])
            event_to_reprocess = head["event"]
            event_to_reprocess["reprocessing"] = {}
            event_to_reprocess["reprocessing"]["executed_at"] = p["startExecution"]
            event_to_reprocess["reprocessing"]["instance_id"] = p["id"]
            event_to_reprocess["reprocessing"]["app_name"] = p["appName"]
            event_to_reprocess["reprocessing"]["process_id"] = p["processId"]
            event_to_reprocess["reprocessing"]["version"] = p["version"]
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

    def persist(self, items):
        repository = Persistence(self.session)
        instances = repository.persist(items)
        repository.commit()
        return instances

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

