from core.component import Component


class Index(Component):
    """ Index map into many data sctructures """

    def __init__(self):
        Component.__init__(self)

        self.model_cache = dict()
        self.projection_cache = dict()
        self.functions_map = dict()
        self.includes_map = dict()
        self.entity_to_map = dict()

    def parse(self, yaml):
        """
            Index yaml map
        """
        self.maps = yaml
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
            add_attr(entity, "rid")
            add_attr(entity, "id")
            add_attr(entity, "meta_instance_id")
            add_attr(entity, "from_id")
            add_attr(entity, "branch")
            add_attr(entity, "modified")
            add_attr(entity, "created_at")
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
                proj = [field_obj['column'], field]
                projections[mapped_model]['attributes'].append(proj)

    def get_map(self, app_id, app_name=None):
        """ returns cached map for an app_id """
        app_map = self.model_cache.get(app_id, {})

        if not app_name:
            return app_map

        return app_map.get(app_name, {})

    def get_projection(self, app_id):
        """ returns projection list of a app_id """
        return self.projection_cache.get(app_id, {})

    def get_filters(self, app_id, map_name):
        """ returns filters on map  """
        if self.has_model_cache(app_id, map_name) and "filters" in self.model_cache[app_id][map_name]:
            return self.model_cache[app_id][map_name]["filters"]
        return dict()

    def get_fields(self, app_id, map_name):
        """ returns map fields by app_id and name """
        if self.has_model_cache(app_id, map_name) and "fields" in self.model_cache[app_id][map_name]:
            return self.model_cache[app_id][map_name]["fields"]
        return dict()

    def get_model_name(self, app_id, map_name):
        """ returns entity models name """
        _map = self.get_map(app_id, map_name)
        return _map.get('model', {})

    def get_functions(self, app_id, map_name):
        """ returns function fields in map """
        if self.has_functions_map(app_id, map_name):
            return self.functions_map[app_id][map_name]
        return dict()

    def get_map_type_by_domain_type(self, app_id, domain_type):
        """ returns mapped name based on domain name """
        if self.has_entity_to_map(app_id, domain_type):
            return self.entity_to_map[app_id][domain_type]
        return ""

    def columns_from_map_type(self, app_id, map_name):
        """ return 1 to 1 map -> domain """
        field_obj = self.model_cache[app_id][map_name]['fields']

        for map_column, map_field in field_obj.items():
            reference = map_field.get('column', map_field.get('type'))

            if reference != "function":
                yield map_column, reference

    def has_entity_to_map(self, app_id, domain_type):
        return app_id in self.entity_to_map and domain_type in self.entity_to_map[app_id]

    def has_functions_map(self, app_id, map_name):
        return app_id in self.functions_map and map_name in self.functions_map[app_id]

    def has_model_cache(self, app_id, map_name):
        return app_id in self.model_cache and map_name in self.model_cache[app_id]
