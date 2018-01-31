from core.component import Component


class Index(Component):

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
        yaml = self.apply_default_fields(yaml)
        self.model_cache[yaml['app_name']] = yaml['map'][yaml['app_name']]

        self.generate_index(yaml)

    def apply_default_fields(self,yaml):
        """
            Apply default fields to map
        """
        def add_attr(entity, attr):
            if not attr in yaml['map'][entity]['fields']:
                yaml['map'][entity]['fields'][attr] = dict()
                yaml['map'][entity]['fields'][attr]['column'] = attr
        for entity in yaml['map']:
            add_attr(entity,"id")
            add_attr(entity,"meta_instance_id")
        return yaml

    def generate_index(self, yaml):
        """
            Index yaml map
        """
        print(yaml)

