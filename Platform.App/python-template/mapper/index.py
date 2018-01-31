from core.component import Component


class Index(Component):
    """ Index map into many data sctructures """

    def __init__(self, maps):
        Component.__init__(self)
        self.maps = maps
        self.model_cache = dict()
        self.projection_cache = dict()
        self.functions_map = dict()
        self.includes_map = dict()
        self.entity_to_map = dict()

    def parse(self, yaml):
        """
            Index yaml map
        """
        for current in self.maps:
            yaml = self.apply_default_fields(current)
            self.model_cache[yaml['app_name']] = yaml['map']
            self.generate_index(yaml)

    def apply_default_fields(self, yaml):
        """
            Apply default fields to map
        """
        def add_attr(entity, attr):
            if not attr in yaml['map'][entity]['fields']:
                yaml['map'][entity]['fields'][attr] = dict()
                yaml['map'][entity]['fields'][attr]['column'] = attr
        for entity in yaml['map']:
            add_attr(entity, "id")
            add_attr(entity, "meta_instance_id")
        return yaml

    def generate_index(self, yaml):
        """
            Index yaml map
        """
        process_id = yaml['app_name']
        _map = yaml['map']
        self.projection_cache[process_id] = dict()
        projections = self.projection_cache[process_id]
        self.entity_to_map[process_id] = dict()
        for mapped_model in _map:
            entity = _map[mapped_model]['model']
            self.entity_to_map[process_id][entity] = mapped_model
            projections[mapped_model] = dict()
            projections[mapped_model]['attributes'] = []
            for field in _map[mapped_model]['fields']:
                field_obj = _map[mapped_model]["fields"][field]
                if 'type' in field_obj and field_obj['type'] == "function":
                    self.functions_map[process_id] = dict()
                    self.functions_map[process_id][mapped_model] = dict()
                    self.functions_map[process_id][mapped_model][field] = field_obj
                    continue
                elif 'type' in field_obj and field_obj['type'] == "include":
                    self.includes_map[process_id] = dict()
                    self.includes_map[process_id][mapped_model] = dict()
                    self.includes_map[process_id][mapped_model][field] = field_obj
                    continue
                proj = [field_obj['column'], field]
                projections[mapped_model]['attributes'].append(proj)
