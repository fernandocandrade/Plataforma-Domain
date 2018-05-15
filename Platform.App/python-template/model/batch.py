from model.persistence import Persistence
from model.domain import *
from sdk import process_memory, event_manager, process_instance, domain_dependency
from mapper.builder import MapBuilder
from dateutil import parser
from datetime import datetime
import pytz
import log


class BatchPersistence:

    def __init__(self,session):
        self.session = session

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
                domain_obj["from_id"] = item.get("fromId")
                domain_obj["modified"] = item["_metadata"].get("modified_at", datetime.utcnow())
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
            processes = self.persist(items)
            log.info("objects persisted")
            parts = self.event["name"].split(".")
            parts.pop()
            parts.append("done")
            name = ".".join(parts)
            log.info(f"pushing event {name} to event manager")
            event_manager.push({"name":self.event_out, "instanceId":instance_id, "payload":{"instance_id":instance_id}})

            processes = self.group_by_process_and_version(processes)
            if len(processes) > 0:
                log.info(f"Reprocessing {len(processes)} instances")

            for p in processes:
                log.info(f"Need to re-execute {p['origin_event_name']} from process {p['appName']} instance {p['id']}")
                head = self.get_head_of_process_memory(p["id"])
                event_to_reprocess = head["event"]
                event_to_reprocess["scope"] = "execution"
                event_to_reprocess["branch"] = p["branch"]
                log.info(event_to_reprocess)
                event_manager.push(event_to_reprocess)

        except Exception as e:
            event_manager.push({"name":"system.process.persist.error", "instanceId":instance_id, "payload":{"instance_id":instance_id, "origin":self.event}})
            log.info("exception occurred")
            log.critical(e)
            raise e


    def group_by_process_and_version(self, processes):
        exist = set()
        result = []
        for p in processes:
            key = f"{p['processId']}:{p['version']}"
            if not key in exist:
                exist.add(key)
                result.append(p)
        return result

    def persist(self, items):
        """
        Identificar qual o b

        """
        processes = self.get_impacted_processes(items)
        repository = Persistence(self.session)
        instances = repository.persist(items)
        repository.commit()
        return processes

    def get_impacted_processes(self, items):
        older_data = pytz.UTC.localize(datetime.utcnow())
        impacted_domain = set()
        current_branch = "master"
        for item in items:
            current_branch = item["_metadata"].get("branch", "master")
            if "modified_at" in item["_metadata"]:
                date = parser.parse(item["_metadata"]["modified_at"])
            else:
                date = pytz.UTC.localize(datetime.utcnow())
            if date < older_data:
                older_data = date
            impacted_domain.add(item["_metadata"]["type"])

        log.info(f"Older data at {older_data}")
        instances =  process_instance.ProcessInstance().get_processes_after(older_data, self.instance_id, self.process_id)
        deps = []
        for instance in instances:
            result = domain_dependency.DomainDependency().get_dependency_by_process_and_version(instance["processId"],instance["version"], impacted_domain)
            if len(result) > 0:
                instance["appName"] = result[0]["name"]
                instance["branch"] = current_branch
                deps.append(instance)
        log.info("--------------------------------------------------------------")
        log.info(deps)
        return deps

