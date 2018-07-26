from model.persistence import Persistence
from model.domain import *
from sdk import process_memory, event_manager, process_instance, domain_dependency
from mapper.builder import MapBuilder
from dateutil import parser
from datetime import datetime
from reprocessing import ReprocessingManager
from sdk import operation
import pytz
import log
from uuid import uuid4
import copy
import hashlib
import json
from utils.pruu import log_on_pruu

class BatchPersistence:

    def __init__(self,session):
        self.session = session
        self.process_id = None
        self.instance_id = None
        self.operationService = operation.Operation()

    def get_head_of_process_memory(self, instance_id):
        return process_memory.head(instance_id)

    def extract_head(self, head):
        self.event = head.get("event",{})
        self.scope = self.event.get("scope")
        if self.scope == None:
            log.info("scope is None")
            log.info(self.event)
            raise "scope not found"
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

    def get_entities(self, instance_id):
        head = self.get_head_of_process_memory(instance_id)
        log.info("extracting data from dataset")
        self.extract_head(head)
        log.info("getting items to persist")
        return self.get_items_to_persist(self.entities, instance_id)

    def run(self, instance_id):
        try:
            log.info(f"getting data from process memory with instance id {instance_id}")
            head = self.get_head_of_process_memory(instance_id)
            log.info("extracting data from dataset")
            self.extract_head(head)
            log.info("getting items to persist")
            items = self.get_items_to_persist(self.entities, instance_id)
            log.info(f"should persist {len(items)} objects in database")
            instances = self.persist(items,self.scope)
            log.info("objects persisted")
            parts = self.event["name"].split(".")
            parts.pop()
            parts.append("done")
            name = ".".join(parts)
            log.info(f"pushing event {name} to event manager")
            operation = self.operationService.find_by_name_and_version(self.event["name"],self.event["version"])
            if not operation:
                raise Exception(f"operation not found from event {self.event['name']} in version {self.event['version']}")
            evt = {"name":operation.event_out, "version":operation.version, "idempotencyKey":self.event["idempotencyKey"],"systemId":self.event["systemId"], "tag":self.event["tag"] , "instanceId":instance_id, "scope":self.event["scope"], "branch": self.event["branch"], "reprocessing":self.event["reprocessing"] , "payload":{"instance_id":instance_id}}
            event_manager.push(evt)
            #ReprocessingManager(self.process_id, self.instance_id).dispatch_reprocessing_events(instances)

        except Exception as e:
            event_manager.push({"name":"system.process.persist.error", "instanceId":instance_id, "payload":{"instance_id":instance_id, "origin":self.event}})
            log.info("exception occurred")
            log.critical(e)
            raise e

    def persist(self, items, scope):
        repository = Persistence(self.session)
        instances = repository.persist(items, scope)
        repository.commit()
        return instances