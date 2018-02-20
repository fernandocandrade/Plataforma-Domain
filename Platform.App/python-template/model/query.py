import re
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
        self.query = None
        self.entity_cls = None

    def set_query_context(self, app_id, mapped_entity, entity):
        self.app_id = app_id
        self.mapped_entity = mapped_entity
        self.entity = entity
        self.entity_cls = getattr(domain, self.entity.title())
        self.query = self.session.query(entity_cls)

    def build_select(self, projection):
        fields = [
            getattr(self.entity_cls, a[0]).label(a[1])
            for a in projection['attributes'] if a[0] != 'meta_instance_id'
        ]

    def execute(self, projection):
        query_select = self.build_select(projection)
        q_ = self.session.query(*query_select)
        if 'where' in projection:
            query = projection["where"]["query"]
            stmt = text(query)
            stmt = stmt.bindparams(**projection["where"]["params"])
            return q_.filter(stmt).all()
        return q_.all()

    def build_where(self, projection):
        params = projection['where']['params']
        params.pop('filter')
        where_clause = projection['where']['query']
        par_regex = re.compile(":\w*")
        #  par_regex = re.compile(":\w*\[\]")

        def build_param(g):
            arr_filter = ""
            current_pars = params.pop('ids')
            for i in range(len(current_pars)):
                lbl_par = f'ids{i}'
                arr_filter += f':{lbl_par},'
                params[lbl_par] = current_pars[i]
            return arr_filter

        #  q_ = q_.filter(text(where_clause).bindparams(**params))


