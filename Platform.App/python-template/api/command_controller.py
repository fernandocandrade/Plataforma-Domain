from model.persistence import Persistence
import json
from mapper.builder import MapBuilder
from database import create_session

from flask import request


class CommandController:
    """ Command Controller persist data on domain """

    def __init__(self, app_id, body, instance_id, reference_date):
        self.app_id = app_id
        self.body = body
        self.mapper = MapBuilder().build()
        self.instance_id = instance_id
        self.repository = Persistence(request.session)
        self.reference_date = reference_date

    def persist(self):
        """ Persist data on domain """
        if not self.body:
            return []

        domain_obj = self.to_domain()
        instances = self.repository.persist(domain_obj)
        self.repository.commit()
        return self.from_domain(instances)

    def to_domain(self):
        for o in self.body:
            curr = self.mapper.translator.to_domain(self.app_id, o)

            if self.instance_id:
                curr["meta_instance_id"] = self.instance_id

            yield curr

    def from_domain(self, instances):
        return [
            self.mapper.translator.to_map(self.app_id, i.dict()) for i in instances
        ]

