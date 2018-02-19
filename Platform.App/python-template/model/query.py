from model import domain
from sqlalchemy.sql import text


class Query:
    def __init__(self, reference_date, version, session):
        self.reference_date = reference_date
        self.version = version
        self.session = session
        self.app_id = None
        self.mapped_entity = None
        self.entity = None

    def set_query_context(self, app_id, mapped_entity, entity):
        self.app_id = app_id
        self.mapped_entity = mapped_entity
        self.entity = entity

    def build_select(self, projection):
        entity_cls = getattr(domain, self.entity.title())

        return [
            getattr(entity_cls, a[0]).label(a[1])
            for a in projection['attributes'] if a[0] != 'meta_instance_id'
        ]

    def build_where(self, projection):
        params = projection['where']['params']
        where_clause = projection['where']['query']
        import re
        arr_regex = r":\w*\[\]"
        matches = re.finditer(arr_regex, where_clause)



        #  p_ids = {f'id{i}': query_['ids'][i] for i in range(len(query_['ids']))}
        #  p_.pop('filter')
        #  q_ = q_.filter(text(filter_).bindparams(**p_ids))

    def execute(self, projection):
        query_select = self.build_select(projection)
        #  q_ = self.session.query(*query_select)

        if 'where' in projection:
            self.build_where(projection)

            #  filter_ = "id in (:ids[])"
            #  query_ = {'ids': [10, 20, 30, 40, 50]}
            #  ff = ', '.join([f':id{i}' for i in range(len(query_['ids']))])
#

        filter_ = filter_.replace(':ids[]', ff)

        return q_.all()


