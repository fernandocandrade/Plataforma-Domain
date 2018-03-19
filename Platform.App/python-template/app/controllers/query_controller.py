""" Query Controller """


class QueryController:
    def __init__(self, app_id, entity, query, mapper, query_service):
        self.app_id = app_id
        self.mapped_entity = entity
        self.page = int(query.pop('page', 0))
        self.page_size = int(query.pop('page_size', 0))
        self.query_string = query
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
        projection['where'] = self.mapper.transform.get_filters(self.app_id, self.mapped_entity, self.query_string)

        if not list(projection["where"].keys()):
            projection.pop('where', None)


        result = self.query_service.filter(self.app_id, self.mapped_entity, entity, projection, self.page, self.page_size)
        #result = self.mapper.transform.apply_runtime_fields(self.app_id,self.mapped_entity,result)
        return result
