from model.persistence import Persistence
import json
from mapper.builder import MapBuilder
from database import create_session
""" Command Controller persist data on domain """


class CommandController:
    def __init__(self, app_id, body, instance_id, reference_date):
        self.app_id = app_id
        self.body = body
        self.mapper =  MapBuilder().build()
        self.instance_id = instance_id
        self.session = create_session()
        self.repository = Persistence(self.session)
        self.reference_date = reference_date

    def persist(self):
        """ Persist data on domain """
        if len(self.body) == 0:
            return []

        domain_obj = self.to_domain()
        instances = self.repository.persist(domain_obj)
        self.repository.commit()
        l = list(self.from_domain(instances))
        return l

    def to_domain(self):
        result = []
        for o in self.body:
            curr = self.mapper.translator.to_domain(self.app_id, o)
            if self.instance_id != None:
                curr["meta_instance_id"] = self.instance_id
            result.append(curr)
        return result

    def from_domain(self, instances):
        for i in instances:
            curr = self.mapper.translator.to_map(self.app_id, i.dict())
            yield curr