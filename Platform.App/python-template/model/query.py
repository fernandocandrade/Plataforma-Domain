import re
from model import domain
from sqlalchemy.sql import text
import uuid
import log

class Query:
    def __init__(self, reference_date, version, session):
        self.reference_date = reference_date
        self.version = version
        self.session = session
        self.app_id = None
        self.mapped_entity = None
        self.entity = None
        self.entity_cls = None

    def set_query_context(self, app_id, mapped_entity, entity):
        self.app_id = app_id
        self.mapped_entity = mapped_entity
        self.entity = entity
        self.entity_cls = getattr(domain, self.entity.lower())

    def build_select(self, projection):
        return [
            getattr(self.entity_cls, a[0]).label(a[1])
            for a in projection['attributes']
        ]

    def execute(self, projection, page=None, page_size=None):
        query_select = self.build_select(projection)
        q_ = self.session.query(*query_select)
        q_ = q_.filter(text("deleted = false"))

        if page and page_size:
            page -= 1
            q_ = q_.slice(page * page_size, page * page_size + page_size)

        if 'where' in projection:
            query = projection["where"]["query"]
            #TODO melhorar a implementação
            stmt = text(query)
            stmt = stmt.bindparams(**projection["where"]["params"])
            resultset = q_.filter(stmt).all()
            return self.row2dict(resultset, projection)

        resultset = q_.all()
        return self.row2dict(resultset, projection)

    def history(self, mapped_entity, entity, projection, entity_id):
        domain_entity = getattr(domain, entity)
        query_select = self.build_select(projection)
        history = self.session.query(domain_entity).history(
            fields=query_select, period=self.reference_date)
        items = history.filter(domain_entity.id==entity_id).all()

        if not items:
            return []

        tree = {f[1]:{} for f in projection['attributes'] if f[1] not in {'id', 'meta_instance_id',}}
        ticks = items[0][1]

        for item in items:
            item_dict = item._asdict()
            for key, tick_range in tree.items():
                tick_range[item_dict[f'{key}_ticks']] = item_dict[key]

        for tick in range(1, ticks + 1):
            obj = {'_metadata': { 'version': tick }}
            for field, tick_tree in tree.items():
                obj.update({field: v for t, v in tick_tree.items() if tick in t})
            yield obj

    def row2dict(self, rows, projection):
        d = {}
        result = []
        for row in rows:
            d = {}
            cont = 0
            instance_id = None
            for column in row:
                if type(column) == uuid.UUID:
                    column = str(column)
                if projection['attributes'][cont][1] == "meta_instance_id":
                    cont += 1
                    instance_id = column
                    continue
                d[projection['attributes'][cont][1]] = column
                cont += 1
            d["_metadata"] = {
                "type": self.mapped_entity,
                "branch":"master"
            }
            if instance_id:
                d["_metadata"]["instance_id"] = instance_id
            result.append(d)
        return result
