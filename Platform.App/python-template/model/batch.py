
from model.persistence import Persistence
from model.domain import *
from sdk import process_memory, event_manager
from mapper.builder import MapBuilder
import log

class BatchPersistence:

    def __init__(self,session):
        self.session = session



    def get_head_of_process_memory(self, instance_id):
        return process_memory.head(instance_id)

    def extract_head(self, head):
        self.event = head.get("event",{})
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



    def get_items_to_persist(self, entities, instance_id):
        """ process head and collect data to persist on domain """
        items = []
        for entity in entities:
            for item in entities[entity]:
                if not self.has_change_track(item):
                    continue
                domain_obj = self.mapper.translator.to_domain(self.map["app_name"], item)
                domain_obj["meta_instance_id"] = instance_id
                items.append(domain_obj)
        return items


    def has_change_track(self, item):
        return "_metadata" in item and "changeTrack" in item['_metadata']


    def run(self, instance_id):
        log.info(f"getting data from process memory with instance id {instance_id}")
        head = self.get_head_of_process_memory(instance_id)
        log.info("extracting data from dataset")
        self.extract_head(head)
        log.info("getting items to persist")
        items = self.get_items_to_persist(self.entities, instance_id)
        log.info(f"should persist {len(items)} objects in database")
        self.persist(items)
        log.info("objects persisted")
        parts = self.event["name"].split(".")
        parts.pop()
        parts.append("done")
        name = ".".join(parts)
        log.info(f"pushing event {name} to event manager")
        event_manager.push({"name":name, "instanceId":instance_id, "payload":{"instance_id":instance_id}})

    def persist(self, items):
        repository = Persistence(self.session)
        instances = repository.persist(items)
        repository.commit()
