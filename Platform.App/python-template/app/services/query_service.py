from model.query import Query


class QueryService:
    def __init__(self, reference_date, version, session, branch='master'):
        self.reference_date = reference_date
        self.version = version
        self.session = session
        self.branch = branch

    def filter(self, app_id, mapped_entity, entity, projection, page=None, page_size=None):
        """ execute a query on domain """
        query = Query(self.reference_date, self.version, self.session, branch=self.branch)
        query.set_query_context(app_id, mapped_entity, entity)

        return query.execute(projection, page=page, page_size=page_size)

    def history(self, app_id, mapped_entity, entity, projection, entity_id, version):
        """ gets an entity history """
        query = Query(self.reference_date, version=None, session=self.session, branch=self.branch)
        query.set_query_context(app_id, mapped_entity, entity)

        return query.history(mapped_entity, entity, projection, entity_id, version)
