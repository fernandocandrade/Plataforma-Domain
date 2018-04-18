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
        attrs = [
            getattr(self.entity_cls, a[0]).label(a[1])
            for a in projection['attributes']
        ]
        return attrs

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
        query_select.append(getattr(self.entity_cls, "deleted").label("destroy"))
        history = self.session.query(domain_entity).history(
            fields=query_select, period=self.reference_date)
        history = history.filter(domain_entity.id==entity_id)

        ranges = []
        for f in query_select:
            parts = str(f.element).split(".")
            n = parts[1]
            if n in ["id"]:
                continue
            ranges.append(entity+n+"history.ticks")
        history = history.filter(f"not isEmpty({' * '.join(ranges)})")

        ticks_fields = {
            c['name'] for c in history.column_descriptions
            if c['name'].endswith('_ticks')
        }
        for entity_history in history.all():
            entity_dict = entity_history._asdict()
            log.info(entity_dict)
            entity_dict["_metadata"] = {}
            entity_dict["_metadata"]["type"] = self.mapped_entity
            entity_dict["_metadata"]['version'] = 0
            entity_dict["_metadata"]["instance_id"] = entity_dict["meta_instance_id"]
            entity_dict["id"] = entity_id
            if entity_dict["destroy"]:
                entity_dict["_metadata"]["destroy"] = entity_dict["destroy"]
            entity_dict.pop(entity)
            entity_dict.pop("destroy")
            entity_dict.pop("meta_instance_id")
            for tick_field in ticks_fields:
                if not entity_dict[tick_field]:
                    entity_dict.pop(tick_field)
                    continue
                entity_dict["_metadata"]['version'] = max(entity_dict["_metadata"]['version'], entity_dict[tick_field])
                entity_dict.pop(tick_field)
            yield entity_dict

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
