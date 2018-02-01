""" Command Controller persist data on domain """
class CommandController:
    def __init__(self, app_id, body, mapper, instance_id):
        self.app_id = app_id
        self.body = body
        self.mapper = mapper
        self.instance_id = instance_id

    def persist(self):
        """ Persist data on domain """
        if len(self.body) == 0:
            return []
        domain_obj = self.to_domain()

        for o in domain_obj:
            o["id"] = "1"
        return domain_obj

    def to_domain(self):
        result = []
        for o in self.body:
            curr = self.mapper.translator.to_domain(self.app_id,o)
            if self.instance_id != None:
                curr["meta_instance_id"] = self.instance_id
            result.append(curr)
        return result
