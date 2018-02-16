class Query:

    def __init__(self, reference_date, version):
        self.reference_date = reference_date
        self.version = version

    def set_query_context(self, app_id, mapped_entity, entity):
        self.app_id = app_id
        self.mapped_entity = mapped_entity
        self.entity = entity

    def execute(self, projection):
        return []
