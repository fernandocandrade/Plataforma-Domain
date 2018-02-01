""" Query Controller """


class QueryController:
    def __init__(self, app_id, entity, request, mapper, query_service):
        self.request = request
        self.app_id = app_id
        self.mapped_entity = entity
        self.req = request
        self.mapper = mapper
        self.query_service = query_service

    def query(self):
        """ query data on domain """
        entity = self.mapper.index.get_model_name(
            self.app_id, self.mapped_entity)
        projection = self.mapper.index.get_projection(self.app_id)
        if not self.mapped_entity in projection:
            raise Exception(f"{self.mapped_entity} not found in map")
        projection = projection[self.mapped_entity]
        projection['where'] = self.mapper.transform.get_filters(self.app_id, self.mapped_entity, self.req.args)
        if not list(projection["where"].keys()):
            projection.pop('where', None)
        return self.query_service.filter(self.app_id, self.mapped_entity, entity, projection)
