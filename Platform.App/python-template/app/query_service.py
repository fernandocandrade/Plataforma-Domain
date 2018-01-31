from model.query import Query


class QueryService:
    def filter(self, app_id, mapped_entity, entity, projection):
        """ execute a query on domain """
        query = Query()
        query.set_query_context(app_id, mapped_entity, entity)
        return Query().execute(projection)
